from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums.flight_status import FlightStatus
from app.domain.value_objects.airport import Airport
from app.domain.value_objects.flight_number import FlightNumber


@dataclass
class Flight:
    flight_number: FlightNumber
    origin: Airport
    destination: Airport
    scheduled_departure: datetime
    scheduled_arrival: datetime
    airline: str
    status: FlightStatus = FlightStatus.SCHEDULED
    gate: str | None = None
    aircraft_type: str | None = None
    actual_departure: datetime | None = None
    actual_arrival: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    flight_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.origin == self.destination:
            raise ValueError(
                "Origin and destination airports must be different.")
        if self.scheduled_departure >= self.scheduled_arrival:
            raise ValueError(
                "Scheduled departure must be before scheduled arrival.")
