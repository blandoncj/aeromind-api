from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_get_flight_use_case, get_search_flights_use_case
from app.application.dtos.flight_dtos import GetFlightInput, SearchFlightsInput
from app.application.use_cases.flights.get_flight import GetFlightUseCase
from app.application.use_cases.flights.search_flights import SearchFlightsUseCase
from app.domain.enums.flight_status import FlightStatus

router = APIRouter(prefix="/flights", tags=["flights"])


class FlightResponse(BaseModel):
    flight_id: UUID
    flight_number: str
    origin: str
    destination: str
    airline: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    status: FlightStatus
    gate: str | None
    aircraft_type: str | None
    actual_departure: datetime | None
    actual_arrival: datetime | None


@router.get("")
async def search_flights(
    origin: str,
    destination: str,
    departure_date: date,
    use_case: Annotated[SearchFlightsUseCase, Depends(get_search_flights_use_case)],
) -> list[FlightResponse]:
    results = await use_case.execute(SearchFlightsInput(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
    ))
    return [FlightResponse(**vars(f)) for f in results]


@router.get("/{flight_id}")
async def get_flight(
    flight_id: UUID,
    use_case: Annotated[GetFlightUseCase, Depends(get_get_flight_use_case)],
) -> FlightResponse:
    result = await use_case.execute(GetFlightInput(flight_id=flight_id))
    return FlightResponse(**vars(result))
