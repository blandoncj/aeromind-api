import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dtos.flight_dtos import FlightOutput, GetFlightInput
from app.application.exceptions.flight_not_found_error import FlightNotFoundError
from app.application.use_cases.flights.get_flight import GetFlightUseCase
from app.domain.enums.flight_status import FlightStatus


def _make_flight(flight_id=None) -> MagicMock:
    flight = MagicMock()
    flight.flight_id = flight_id or uuid4()
    flight.flight_number.value = "AV123"
    flight.origin.code = "BOG"
    flight.destination.code = "MIA"
    flight.airline = "Avianca"
    flight.scheduled_departure = datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc)
    flight.scheduled_arrival = datetime(2026, 6, 1, 14, 0, tzinfo=timezone.utc)
    flight.status = FlightStatus.SCHEDULED
    flight.gate = "A12"
    flight.aircraft_type = "A320"
    flight.actual_departure = None
    flight.actual_arrival = None
    return flight


class TestGetFlightUseCase:
    def test_returns_flight_output(self) -> None:
        flight_id = uuid4()
        flight = _make_flight(flight_id)
        repo = AsyncMock()
        repo.find_by_id.return_value = flight

        result = asyncio.run(GetFlightUseCase(repo).execute(GetFlightInput(flight_id)))

        assert isinstance(result, FlightOutput)
        assert result.flight_id == flight_id
        assert result.flight_number == "AV123"
        assert result.origin == "BOG"
        assert result.destination == "MIA"

    def test_raises_when_flight_not_found(self) -> None:
        repo = AsyncMock()
        repo.find_by_id.return_value = None
        flight_id = uuid4()

        with pytest.raises(FlightNotFoundError) as exc_info:
            asyncio.run(GetFlightUseCase(repo).execute(GetFlightInput(flight_id)))

        assert exc_info.value.code == "FLIGHT_NOT_FOUND"
        assert str(flight_id) in exc_info.value.context["flight_id"]

    def test_queries_repository_with_correct_id(self) -> None:
        flight_id = uuid4()
        repo = AsyncMock()
        repo.find_by_id.return_value = _make_flight(flight_id)

        asyncio.run(GetFlightUseCase(repo).execute(GetFlightInput(flight_id)))

        repo.find_by_id.assert_called_once_with(flight_id)
