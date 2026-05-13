from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.baggage_type import BaggageType


@dataclass(frozen=True)
class TrackBaggageInput:
    tag: str


@dataclass(frozen=True)
class ReportLostBaggageInput:
    tag: str
    reported_by: UUID
    description: str | None = None


@dataclass(frozen=True)
class BaggageOutput:
    baggage_id: UUID
    booking_id: UUID
    tag: str
    baggage_type: BaggageType
    weight_kg: float
    status: BaggageStatus
    description: str | None


@dataclass(frozen=True)
class ReportLostBaggageOutput:
    baggage_id: UUID
    tag: str
    incident_id: UUID
