import asyncio
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from app.application.dtos.flight_dtos import FlightOutput, SearchFlightsInput
from app.application.use_cases.flights.search_flights import SearchFlightsUseCase
from app.domain.enums.flight_status import FlightStatus
from app.domain.value_objects.airport import Airport


def _make_flight(number: str = "AV123") -> MagicMock:
    flight = MagicMock()
    flight.flight_number.value = number
    flight.origin.code = "BOG"
    flight.destination.code = "MIA"
    flight.airline = "Avianca"
    flight.scheduled_departure = datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc)
    flight.scheduled_arrival = datetime(2026, 6, 1, 14, 0, tzinfo=timezone.utc)
    flight.status = FlightStatus.SCHEDULED
    flight.gate = None
    flight.aircraft_type = None
    flight.actual_departure = None
    flight.actual_arrival = None
    return flight


class TestSearchFlightsUseCase:
    def test_returns_list_of_flight_outputs(self) -> None:
        repo = AsyncMock()
        repo.search.return_value = [_make_flight("AV123"), _make_flight("AV456")]

        result = asyncio.run(
            SearchFlightsUseCase(repo).execute(
                SearchFlightsInput(origin="BOG", destination="MIA", departure_date=date(2026, 6, 1))
            )
        )

        assert len(result) == 2
        assert all(isinstance(f, FlightOutput) for f in result)
        assert result[0].flight_number == "AV123"
        assert result[1].flight_number == "AV456"

    def test_returns_empty_list_when_no_flights(self) -> None:
        repo = AsyncMock()
        repo.search.return_value = []

        result = asyncio.run(
            SearchFlightsUseCase(repo).execute(
                SearchFlightsInput(origin="BOG", destination="MIA", departure_date=date(2026, 6, 1))
            )
        )

        assert result == []

    def test_passes_airport_value_objects_to_repository(self) -> None:
        repo = AsyncMock()
        repo.search.return_value = []
        departure = date(2026, 6, 1)

        asyncio.run(
            SearchFlightsUseCase(repo).execute(
                SearchFlightsInput(origin="BOG", destination="MIA", departure_date=departure)
            )
        )

        call_kwargs = repo.search.call_args
        assert call_kwargs.kwargs["origin"] == Airport("BOG")
        assert call_kwargs.kwargs["destination"] == Airport("MIA")
        assert call_kwargs.kwargs["departure_date"] == departure
