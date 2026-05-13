from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class DocumentChunk:
    document_id: UUID
    content: str
    chunk_index: int
    embedding: list[float]
    chunk_id: UUID = field(default_factory=uuid4)
