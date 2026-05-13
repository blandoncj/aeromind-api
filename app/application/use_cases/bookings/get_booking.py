from app.application.dtos.booking_dtos import BookingOutput, GetBookingInput
from app.application.exceptions.booking_not_found_error import BookingNotFoundError
from app.application.ports.booking_repository import BookingRepository
from app.domain.entities.booking import Booking
from app.domain.value_objects.booking_reference import BookingReference


def _to_output(booking: Booking) -> BookingOutput:
    return BookingOutput(
        booking_id=booking.booking_id,
        user_id=booking.user_id,
        flight_id=booking.flight_id,
        booking_reference=booking.booking_reference.value,
        cabin_class=booking.cabin_class,
        status=booking.status,
        seat_number=booking.seat_number.value if booking.seat_number else None,
        created_at=booking.created_at,
    )


class GetBookingUseCase:
    def __init__(self, booking_repository: BookingRepository) -> None:
        self._booking_repository = booking_repository

    async def execute(self, input: GetBookingInput) -> BookingOutput:
        reference = BookingReference(input.booking_reference)
        booking = await self._booking_repository.find_by_reference(reference)
        if booking is None:
            raise BookingNotFoundError(reference.value)
        return _to_output(booking)
