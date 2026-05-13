import pytest

from app.domain.exceptions.invalid_airport_code_error import InvalidAirportCodeError
from app.domain.value_objects.airport import Airport


class TestAirport:
    def test_valid_airport_code(self) -> None:
        airport = Airport("BOG")
        assert airport.code == "BOG"

    def test_normalizes_lowercase_input(self) -> None:
        airport = Airport("mia")
        assert airport.code == "MIA"

    def test_normalizes_whitespace(self) -> None:
        airport = Airport("  JFK  ")
        assert airport.code == "JFK"

    def test_raises_when_two_letters(self) -> None:
        with pytest.raises(InvalidAirportCodeError) as exc_info:
            Airport("BO")
        assert exc_info.value.code == "INVALID_AIRPORT_CODE"

    def test_raises_when_four_letters(self) -> None:
        with pytest.raises(InvalidAirportCodeError):
            Airport("BOGD")

    def test_raises_when_contains_digit(self) -> None:
        with pytest.raises(InvalidAirportCodeError):
            Airport("B0G")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidAirportCodeError):
            Airport("")

    def test_equality_by_code(self) -> None:
        assert Airport("BOG") == Airport("bog")

    def test_immutable(self) -> None:
        airport = Airport("BOG")
        with pytest.raises(Exception):
            airport.code = "MIA"  # type: ignore[misc]
