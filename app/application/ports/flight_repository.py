from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from app.domain.entities.flight import Flight
from app.domain.value_objects.airport import Airport


class FlightRepository(ABC):
    @abstractmethod
    async def find_by_id(self, flight_id: UUID) -> Flight | None: ...

    @abstractmethod
    async def search(
        self,
        origin: Airport,
        destination: Airport,
        departure_date: date,
    ) -> list[Flight]: ...
