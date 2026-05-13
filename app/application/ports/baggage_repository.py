from abc import ABC, abstractmethod

from app.domain.entities.baggage import Baggage
from app.domain.value_objects.baggage_tag import BaggageTag


class BaggageRepository(ABC):
    @abstractmethod
    async def find_by_tag(self, tag: BaggageTag) -> Baggage | None: ...

    @abstractmethod
    async def save(self, baggage: Baggage) -> None: ...
