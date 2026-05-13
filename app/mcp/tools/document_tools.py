from mcp.server.fastmcp import FastMCP

from app.application.dtos.document_dtos import SearchDocumentsInput
from app.application.use_cases.documents.search_documents import SearchDocumentsUseCase
from app.infrastructure.database.session import AsyncSessionFactory
from app.infrastructure.repositories.sqlalchemy_document_repository import (
    SqlAlchemyDocumentRepository,
)
from app.infrastructure.services.gemini_embedding_service import GeminiEmbeddingService
from app.mcp.tools._utils import serialize


def register_document_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def search_policies(query: str, limit: int = 5) -> str:
        """Search airport policies, regulations, and FAQs using semantic search.

        Args:
            query: Natural language question or topic to search for
            limit: Number of relevant fragments to return (default 5)
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyDocumentRepository(session)
                embedding_service = GeminiEmbeddingService()
                results = await SearchDocumentsUseCase(repo, embedding_service).execute(
                    SearchDocumentsInput(query=query, limit=limit)
                )
        return serialize(results)
