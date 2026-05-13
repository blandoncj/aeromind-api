import pytest
from datetime import datetime

from app.domain.entities.flight import Flight
from app.domain.enums.flight_status import FlightStatus
from app.domain.value_objects.airport import Airport
from app.domain.value_objects.flight_number import FlightNumber


_DEPARTURE = datetime(2026, 6, 1, 10, 0)
_ARRIVAL = datetime(2026, 6, 1, 13, 0)
_ORIGIN = Airport("BOG")
_DESTINATION = Airport("MIA")
_FLIGHT_NUMBER = FlightNumber("AV123")


def _make_flight(**overrides) -> Flight:  # type: ignore[no-untyped-def]
    defaults = {
        "flight_number": _FLIGHT_NUMBER,
        "origin": _ORIGIN,
        "destination": _DESTINATION,
        "scheduled_departure": _DEPARTURE,
        "scheduled_arrival": _ARRIVAL,
        "airline": "Avianca",
    }
    defaults.update(overrides)
    return Flight(**defaults)


class TestFlight:
    def test_creates_flight_with_defaults(self) -> None:
        flight = _make_flight()
        assert flight.status == FlightStatus.SCHEDULED
        assert flight.gate is None
        assert flight.aircraft_type is None
        assert flight.actual_departure is None
        assert flight.actual_arrival is None

    def test_flight_id_is_assigned(self) -> None:
        flight = _make_flight()
        assert flight.flight_id is not None

    def test_two_flights_have_different_ids(self) -> None:
        assert _make_flight().flight_id != _make_flight().flight_id

    def test_creates_flight_with_optional_fields(self) -> None:
        flight = _make_flight(gate="23B", aircraft_type="Boeing 737")
        assert flight.gate == "23B"
        assert flight.aircraft_type == "Boeing 737"

    def test_raises_when_origin_equals_destination(self) -> None:
        with pytest.raises(ValueError, match="Origin and destination"):
            _make_flight(origin=Airport("BOG"), destination=Airport("BOG"))

    def test_raises_when_departure_after_arrival(self) -> None:
        with pytest.raises(ValueError, match="departure must be before"):
            _make_flight(
                scheduled_departure=_ARRIVAL,
                scheduled_arrival=_DEPARTURE,
            )

    def test_raises_when_departure_equals_arrival(self) -> None:
        with pytest.raises(ValueError, match="departure must be before"):
            _make_flight(
                scheduled_departure=_DEPARTURE,
                scheduled_arrival=_DEPARTURE,
            )

    def test_status_can_be_set(self) -> None:
        flight = _make_flight(status=FlightStatus.DELAYED)
        assert flight.status == FlightStatus.DELAYED
