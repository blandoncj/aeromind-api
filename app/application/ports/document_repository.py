from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.document import Document
from app.domain.entities.document_chunk import DocumentChunk


class DocumentRepository(ABC):
    @abstractmethod
    async def save_document(self, document: Document) -> None: ...

    @abstractmethod
    async def save_chunks(self, chunks: list[DocumentChunk]) -> None: ...

    @abstractmethod
    async def find_similar_chunks(
        self,
        embedding: list[float],
        limit: int,
    ) -> list[DocumentChunk]: ...

    @abstractmethod
    async def find_by_id(self, document_id: UUID) -> Document | None: ...
