from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from pydantic import BaseModel

from app.api.auth import CurrentUserDep, require_roles
from app.api.dependencies import get_ingest_document_use_case, get_search_documents_use_case
from app.application.dtos.document_dtos import IngestDocumentInput, SearchDocumentsInput
from app.application.use_cases.documents.ingest_document import IngestDocumentUseCase
from app.application.use_cases.documents.search_documents import SearchDocumentsUseCase
from app.domain.enums.role import Role

router = APIRouter(prefix="/documents", tags=["documents"])


class IngestDocumentRequest(BaseModel):
    title: str
    content: str
    source: str


class IngestDocumentResponse(BaseModel):
    document_id: UUID
    title: str
    chunks_created: int
    created_at: datetime


class SearchDocumentsRequest(BaseModel):
    query: str
    limit: int = 5


class SearchDocumentsResponse(BaseModel):
    chunk_id: UUID
    document_id: UUID
    content: str
    chunk_index: int


@router.post(
    "",
    status_code=http_status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.ADMIN))],
)
async def ingest_document(
    body: IngestDocumentRequest,
    use_case: Annotated[IngestDocumentUseCase, Depends(get_ingest_document_use_case)],
    _: CurrentUserDep,
) -> IngestDocumentResponse:
    result = await use_case.execute(IngestDocumentInput(
        title=body.title,
        content=body.content,
        source=body.source,
    ))
    return IngestDocumentResponse(**vars(result))


@router.post("/search")
async def search_documents(
    body: SearchDocumentsRequest,
    use_case: Annotated[SearchDocumentsUseCase, Depends(get_search_documents_use_case)],
    _: CurrentUserDep,
) -> list[SearchDocumentsResponse]:
    results = await use_case.execute(SearchDocumentsInput(
        query=body.query,
        limit=body.limit,
    ))
    return [SearchDocumentsResponse(**vars(r)) for r in results]
