from app.application.dtos.booking_dtos import (
    BookingOutput, GetUserBookingsInput)
from app.application.ports.booking_repository import BookingRepository


class GetUserBookingsUseCase:
    def __init__(self, booking_repository: BookingRepository) -> None:
        self._booking_repository = booking_repository

    async def execute(
            self, input: GetUserBookingsInput) -> list[BookingOutput]:
        bookings = await self._booking_repository.find_by_user_id(
            input.user_id)
        return [
            BookingOutput(
                booking_id=b.booking_id,
                user_id=b.user_id,
                flight_id=b.flight_id,
                booking_reference=b.booking_reference.value,
                cabin_class=b.cabin_class,
                status=b.status,
                seat_number=b.seat_number.value if b.seat_number else None,
                created_at=b.created_at,
            )
            for b in bookings
        ]
