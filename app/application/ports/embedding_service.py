from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...
