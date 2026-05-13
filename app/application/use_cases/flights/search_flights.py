from app.application.dtos.flight_dtos import FlightOutput, SearchFlightsInput
from app.application.ports.flight_repository import FlightRepository
from app.domain.value_objects.airport import Airport


class SearchFlightsUseCase:
    def __init__(self, flight_repository: FlightRepository) -> None:
        self._flight_repository = flight_repository

    async def execute(self, input: SearchFlightsInput) -> list[FlightOutput]:
        flights = await self._flight_repository.search(
            origin=Airport(input.origin),
            destination=Airport(input.destination),
            departure_date=input.departure_date,
        )
        return [
            FlightOutput(
                flight_id=f.flight_id,
                flight_number=f.flight_number.value,
                origin=f.origin.code,
                destination=f.destination.code,
                airline=f.airline,
                scheduled_departure=f.scheduled_departure,
                scheduled_arrival=f.scheduled_arrival,
                status=f.status,
                gate=f.gate,
                aircraft_type=f.aircraft_type,
                actual_departure=f.actual_departure,
                actual_arrival=f.actual_arrival,
            )
            for f in flights
        ]
