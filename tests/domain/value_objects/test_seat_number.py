import pytest

from app.domain.exceptions.invalid_seat_number_error import InvalidSeatNumberError
from app.domain.value_objects.seat_number import SeatNumber


class TestSeatNumber:
    def test_valid_single_digit_row(self) -> None:
        seat = SeatNumber("1A")
        assert seat.value == "1A"

    def test_valid_two_digit_row(self) -> None:
        seat = SeatNumber("12C")
        assert seat.value == "12C"

    def test_valid_max_row(self) -> None:
        seat = SeatNumber("99F")
        assert seat.value == "99F"

    def test_normalizes_lowercase(self) -> None:
        seat = SeatNumber("12c")
        assert seat.value == "12C"

    def test_normalizes_whitespace(self) -> None:
        seat = SeatNumber("  5B  ")
        assert seat.value == "5B"

    def test_raises_when_row_zero(self) -> None:
        with pytest.raises(InvalidSeatNumberError) as exc_info:
            SeatNumber("0A")
        assert exc_info.value.code == "INVALID_SEAT_NUMBER"

    def test_raises_when_row_100(self) -> None:
        with pytest.raises(InvalidSeatNumberError):
            SeatNumber("100A")

    def test_raises_when_letter_out_of_range(self) -> None:
        with pytest.raises(InvalidSeatNumberError):
            SeatNumber("12G")

    def test_raises_when_no_letter(self) -> None:
        with pytest.raises(InvalidSeatNumberError):
            SeatNumber("12")

    def test_raises_when_only_letter(self) -> None:
        with pytest.raises(InvalidSeatNumberError):
            SeatNumber("A")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidSeatNumberError):
            SeatNumber("")

    def test_equality_by_value(self) -> None:
        assert SeatNumber("12A") == SeatNumber("12a")

    def test_immutable(self) -> None:
        seat = SeatNumber("12A")
        with pytest.raises(Exception):
            seat.value = "34B"  # type: ignore[misc]
