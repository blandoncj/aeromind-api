from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.booking_status import BookingStatus
from app.domain.enums.cabin_class import CabinClass


@dataclass(frozen=True)
class GetBookingInput:
    booking_reference: str


@dataclass(frozen=True)
class GetUserBookingsInput:
    user_id: UUID


@dataclass(frozen=True)
class BookingOutput:
    booking_id: UUID
    user_id: UUID
    flight_id: UUID
    booking_reference: str
    cabin_class: CabinClass
    status: BookingStatus
    seat_number: str | None
    created_at: datetime
