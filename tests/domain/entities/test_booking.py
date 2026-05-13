from uuid import uuid4

from app.domain.entities.booking import Booking
from app.domain.enums.booking_status import BookingStatus
from app.domain.enums.cabin_class import CabinClass
from app.domain.value_objects.booking_reference import BookingReference
from app.domain.value_objects.seat_number import SeatNumber


_USER_ID = uuid4()
_FLIGHT_ID = uuid4()
_REFERENCE = BookingReference("ABC123")


def _make_booking(**overrides) -> Booking:  # type: ignore[no-untyped-def]
    defaults = {
        "user_id": _USER_ID,
        "flight_id": _FLIGHT_ID,
        "booking_reference": _REFERENCE,
        "cabin_class": CabinClass.ECONOMY,
    }
    defaults.update(overrides)
    return Booking(**defaults)


class TestBooking:
    def test_creates_booking_with_defaults(self) -> None:
        booking = _make_booking()
        assert booking.status == BookingStatus.CONFIRMED
        assert booking.seat_number is None

    def test_booking_id_is_assigned(self) -> None:
        booking = _make_booking()
        assert booking.booking_id is not None

    def test_two_bookings_have_different_ids(self) -> None:
        assert _make_booking().booking_id != _make_booking().booking_id

    def test_creates_booking_with_seat(self) -> None:
        booking = _make_booking(seat_number=SeatNumber("12A"))
        assert booking.seat_number == SeatNumber("12A")

    def test_creates_booking_with_business_class(self) -> None:
        booking = _make_booking(cabin_class=CabinClass.BUSINESS)
        assert booking.cabin_class == CabinClass.BUSINESS

    def test_creates_booking_with_cancelled_status(self) -> None:
        booking = _make_booking(status=BookingStatus.CANCELLED)
        assert booking.status == BookingStatus.CANCELLED

    def test_references_user_and_flight_by_id(self) -> None:
        booking = _make_booking()
        assert booking.user_id == _USER_ID
        assert booking.flight_id == _FLIGHT_ID
