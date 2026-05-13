from app.agents.base_agent import BaseAgent
from app.application.dtos.document_dtos import SearchDocumentsInput
from app.application.use_cases.documents.search_documents import SearchDocumentsUseCase
from app.infrastructure.repositories.sqlalchemy_document_repository import (
    SqlAlchemyDocumentRepository,
)
from app.infrastructure.services.gemini_embedding_service import GeminiEmbeddingService
from app.mcp.tools._utils import serialize
from google.genai import types


class RagAgent(BaseAgent):
    def _tool_declarations(self) -> list[types.FunctionDeclaration]:
        return [
            types.FunctionDeclaration(
                name="search_policies",
                description="Busca en los documentos y políticas del aeropuerto usando búsqueda semántica",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "query": types.Schema(type="STRING", description="Pregunta o tema a buscar"),
                        "limit": types.Schema(type="INTEGER", description="Número de fragmentos a retornar (default 3)"),
                    },
                    required=["query"],
                ),
            ),
        ]

    async def _execute_tool(self, name: str, args: dict[str, str]) -> str:
        if name == "search_policies":
            repo = SqlAlchemyDocumentRepository(self._session)
            embedding_service = GeminiEmbeddingService()
            results = await SearchDocumentsUseCase(repo, embedding_service).execute(
                SearchDocumentsInput(
                    query=args["query"],
                    limit=int(args.get("limit", 3)),
                )
            )
            return serialize(results)
        return "Herramienta no encontrada."
