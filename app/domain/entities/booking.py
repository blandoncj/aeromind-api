from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums.booking_status import BookingStatus
from app.domain.enums.cabin_class import CabinClass
from app.domain.value_objects.booking_reference import BookingReference
from app.domain.value_objects.seat_number import SeatNumber


@dataclass
class Booking:
    user_id: UUID
    flight_id: UUID
    booking_reference: BookingReference
    cabin_class: CabinClass
    status: BookingStatus = BookingStatus.CONFIRMED
    seat_number: SeatNumber | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    booking_id: UUID = field(default_factory=uuid4)
