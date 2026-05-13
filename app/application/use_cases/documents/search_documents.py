from app.application.dtos.document_dtos import SearchDocumentsInput, SearchDocumentsOutput
from app.application.ports.document_repository import DocumentRepository
from app.application.ports.embedding_service import EmbeddingService


class SearchDocumentsUseCase:
    def __init__(
        self,
        document_repository: DocumentRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        self._document_repository = document_repository
        self._embedding_service = embedding_service

    async def execute(self, input: SearchDocumentsInput) -> list[SearchDocumentsOutput]:
        query_embedding = await self._embedding_service.embed(input.query)
        chunks = await self._document_repository.find_similar_chunks(
            embedding=query_embedding,
            limit=input.limit,
        )
        return [
            SearchDocumentsOutput(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                content=chunk.content,
                chunk_index=chunk.chunk_index,
            )
            for chunk in chunks
        ]
