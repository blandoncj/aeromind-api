import pytest

from app.domain.exceptions.invalid_flight_number_error import InvalidFlightNumberError
from app.domain.value_objects.flight_number import FlightNumber


class TestFlightNumber:
    def test_valid_flight_number(self) -> None:
        fn = FlightNumber("AA123")
        assert fn.value == "AA123"

    def test_normalizes_lowercase_input(self) -> None:
        fn = FlightNumber("la2345")
        assert fn.value == "LA2345"

    def test_normalizes_whitespace(self) -> None:
        fn = FlightNumber("  IB3  ")
        assert fn.value == "IB3"

    def test_single_digit_is_valid(self) -> None:
        fn = FlightNumber("UA1")
        assert fn.value == "UA1"

    def test_four_digit_is_valid(self) -> None:
        fn = FlightNumber("AV9999")
        assert fn.value == "AV9999"

    def test_raises_when_missing_digits(self) -> None:
        with pytest.raises(InvalidFlightNumberError) as exc_info:
            FlightNumber("AA")
        assert exc_info.value.code == "INVALID_FLIGHT_NUMBER"

    def test_raises_when_five_digits(self) -> None:
        with pytest.raises(InvalidFlightNumberError):
            FlightNumber("AA12345")

    def test_raises_when_only_digits(self) -> None:
        with pytest.raises(InvalidFlightNumberError):
            FlightNumber("12345")

    def test_raises_when_one_letter_prefix(self) -> None:
        with pytest.raises(InvalidFlightNumberError):
            FlightNumber("A123")

    def test_raises_when_three_letter_prefix(self) -> None:
        with pytest.raises(InvalidFlightNumberError):
            FlightNumber("AAA123")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidFlightNumberError):
            FlightNumber("")

    def test_equality_by_value(self) -> None:
        assert FlightNumber("AA100") == FlightNumber("aa100")

    def test_immutable(self) -> None:
        fn = FlightNumber("AA100")
        with pytest.raises(Exception):
            fn.value = "BB200"  # type: ignore[misc]
