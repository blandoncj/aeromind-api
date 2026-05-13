from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.document_repository import DocumentRepository
from app.domain.entities.document import Document
from app.domain.entities.document_chunk import DocumentChunk
from app.infrastructure.database.models.document_model import (
    DocumentChunkModel,
    DocumentModel,
)


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_document(self, document: Document) -> None:
        self._session.add(DocumentModel(
            document_id=document.document_id,
            title=document.title,
            content=document.content,
            source=document.source,
            created_at=document.created_at,
        ))

    async def save_chunks(self, chunks: list[DocumentChunk]) -> None:
        for chunk in chunks:
            self._session.add(DocumentChunkModel(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                content=chunk.content,
                chunk_index=chunk.chunk_index,
                embedding=chunk.embedding,
            ))

    async def find_similar_chunks(
        self,
        embedding: list[float],
        limit: int,
    ) -> list[DocumentChunk]:
        result = await self._session.execute(
            select(DocumentChunkModel)
            .order_by(DocumentChunkModel.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        return [self._chunk_to_entity(m) for m in result.scalars().all()]

    async def find_by_id(self, document_id: UUID) -> Document | None:
        model = await self._session.get(DocumentModel, document_id)
        return self._doc_to_entity(model) if model else None

    def _doc_to_entity(self, model: DocumentModel) -> Document:
        return Document(
            document_id=model.document_id,
            title=model.title,
            content=model.content,
            source=model.source,
            created_at=model.created_at,
        )

    def _chunk_to_entity(self, model: DocumentChunkModel) -> DocumentChunk:
        return DocumentChunk(
            chunk_id=model.chunk_id,
            document_id=model.document_id,
            content=model.content,
            chunk_index=model.chunk_index,
            embedding=list(model.embedding),
        )
