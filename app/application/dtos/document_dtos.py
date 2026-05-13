from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class IngestDocumentInput:
    title: str
    content: str
    source: str


@dataclass(frozen=True)
class IngestDocumentOutput:
    document_id: UUID
    title: str
    chunks_created: int
    created_at: datetime


@dataclass(frozen=True)
class SearchDocumentsInput:
    query: str
    limit: int = 5


@dataclass(frozen=True)
class SearchDocumentsOutput:
    chunk_id: UUID
    document_id: UUID
    content: str
    chunk_index: int
