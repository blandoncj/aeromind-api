from app.application.dtos.flight_dtos import FlightOutput, GetFlightInput
from app.application.exceptions.flight_not_found_error import (
    FlightNotFoundError)
from app.application.ports.flight_repository import FlightRepository
from app.domain.entities.flight import Flight


def _to_output(flight: Flight) -> FlightOutput:
    return FlightOutput(
        flight_id=flight.flight_id,
        flight_number=flight.flight_number.value,
        origin=flight.origin.code,
        destination=flight.destination.code,
        airline=flight.airline,
        scheduled_departure=flight.scheduled_departure,
        scheduled_arrival=flight.scheduled_arrival,
        status=flight.status,
        gate=flight.gate,
        aircraft_type=flight.aircraft_type,
        actual_departure=flight.actual_departure,
        actual_arrival=flight.actual_arrival,
    )


class GetFlightUseCase:
    def __init__(self, flight_repository: FlightRepository) -> None:
        self._flight_repository = flight_repository

    async def execute(self, input: GetFlightInput) -> FlightOutput:
        flight = await self._flight_repository.find_by_id(input.flight_id)
        if flight is None:
            raise FlightNotFoundError(input.flight_id)
        return _to_output(flight)
