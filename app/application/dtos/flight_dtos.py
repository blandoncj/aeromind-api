from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.domain.enums.flight_status import FlightStatus


@dataclass(frozen=True)
class SearchFlightsInput:
    origin: str
    destination: str
    departure_date: date


@dataclass(frozen=True)
class GetFlightInput:
    flight_id: UUID


@dataclass(frozen=True)
class FlightOutput:
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
