from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.booking import Booking
from app.domain.value_objects.booking_reference import BookingReference


class BookingRepository(ABC):
    @abstractmethod
    async def find_by_reference(
        self, reference: BookingReference) -> Booking | None: ...

    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> list[Booking]: ...
