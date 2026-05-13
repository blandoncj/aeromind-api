import pytest

from app.domain.exceptions.invalid_booking_reference_error import (
    InvalidBookingReferenceError,
)
from app.domain.value_objects.booking_reference import BookingReference


class TestBookingReference:
    def test_valid_alphanumeric(self) -> None:
        ref = BookingReference("ABC123")
        assert ref.value == "ABC123"

    def test_valid_all_letters(self) -> None:
        ref = BookingReference("XYZABC")
        assert ref.value == "XYZABC"

    def test_valid_all_digits(self) -> None:
        ref = BookingReference("123456")
        assert ref.value == "123456"

    def test_normalizes_lowercase(self) -> None:
        ref = BookingReference("abc123")
        assert ref.value == "ABC123"

    def test_normalizes_whitespace(self) -> None:
        ref = BookingReference("  XY12Z9  ")
        assert ref.value == "XY12Z9"

    def test_raises_when_five_chars(self) -> None:
        with pytest.raises(InvalidBookingReferenceError) as exc_info:
            BookingReference("ABC12")
        assert exc_info.value.code == "INVALID_BOOKING_REFERENCE"

    def test_raises_when_seven_chars(self) -> None:
        with pytest.raises(InvalidBookingReferenceError):
            BookingReference("ABC1234")

    def test_raises_when_contains_special_char(self) -> None:
        with pytest.raises(InvalidBookingReferenceError):
            BookingReference("ABC-12")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidBookingReferenceError):
            BookingReference("")

    def test_equality_by_value(self) -> None:
        assert BookingReference("ABC123") == BookingReference("abc123")

    def test_immutable(self) -> None:
        ref = BookingReference("ABC123")
        with pytest.raises(Exception):
            ref.value = "XYZ999"  # type: ignore[misc]
