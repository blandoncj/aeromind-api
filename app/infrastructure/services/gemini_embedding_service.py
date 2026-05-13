from google import genai

from app.application.ports.embedding_service import EmbeddingService
from app.infrastructure.config.settings import settings


class GeminiEmbeddingService(EmbeddingService):
    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.google_api_key)
        self._model = settings.google_embedding_model

    async def embed(self, text: str) -> list[float]:
        response = await self._client.aio.models.embed_content(
            model=self._model,
            contents=text,
        )
        if not response.embeddings:
            raise ValueError("Gemini returned no embeddings")
        values = response.embeddings[0].values
        return list(values) if values else []
