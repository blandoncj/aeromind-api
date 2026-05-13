from app.application.dtos.document_dtos import IngestDocumentInput, IngestDocumentOutput
from app.application.ports.document_repository import DocumentRepository
from app.application.ports.embedding_service import EmbeddingService
from app.domain.entities.document import Document
from app.domain.entities.document_chunk import DocumentChunk

_CHUNK_SIZE = 500
_CHUNK_OVERLAP = 50


def _split_into_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + _CHUNK_SIZE
        chunks.append(text[start:end].strip())
        start += _CHUNK_SIZE - _CHUNK_OVERLAP
    return [c for c in chunks if c]


class IngestDocumentUseCase:
    def __init__(
        self,
        document_repository: DocumentRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        self._document_repository = document_repository
        self._embedding_service = embedding_service

    async def execute(self, input: IngestDocumentInput) -> IngestDocumentOutput:
        document = Document(
            title=input.title,
            content=input.content,
            source=input.source,
        )
        await self._document_repository.save_document(document)

        raw_chunks = _split_into_chunks(input.content)
        chunks: list[DocumentChunk] = []
        for index, chunk_text in enumerate(raw_chunks):
            embedding = await self._embedding_service.embed(chunk_text)
            chunks.append(DocumentChunk(
                document_id=document.document_id,
                content=chunk_text,
                chunk_index=index,
                embedding=embedding,
            ))

        await self._document_repository.save_chunks(chunks)

        return IngestDocumentOutput(
            document_id=document.document_id,
            title=document.title,
            chunks_created=len(chunks),
            created_at=document.created_at,
        )
