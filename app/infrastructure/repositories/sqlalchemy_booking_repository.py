from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.booking_repository import BookingRepository
from app.domain.entities.booking import Booking
from app.domain.enums.booking_status import BookingStatus
from app.domain.enums.cabin_class import CabinClass
from app.domain.value_objects.booking_reference import BookingReference
from app.domain.value_objects.seat_number import SeatNumber
from app.infrastructure.database.models.booking_model import BookingModel


class SqlAlchemyBookingRepository(BookingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_reference(
            self, reference: BookingReference) -> Booking | None:
        result = await self._session.execute(
            select(BookingModel).where(
                BookingModel.booking_reference == reference.value
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_user_id(self, user_id: UUID) -> list[Booking]:
        result = await self._session.execute(
            select(BookingModel).where(BookingModel.user_id == user_id)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    def _to_entity(self, model: BookingModel) -> Booking:
        return Booking(
            booking_id=model.booking_id,
            user_id=model.user_id,
            flight_id=model.flight_id,
            booking_reference=BookingReference(value=model.booking_reference),
            cabin_class=CabinClass(model.cabin_class),
            status=BookingStatus(model.status),
            seat_number=SeatNumber(
                value=model.seat_number) if model.seat_number else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
