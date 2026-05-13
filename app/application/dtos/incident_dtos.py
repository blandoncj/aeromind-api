from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType


@dataclass(frozen=True)
class CreateIncidentInput:
    reported_by: UUID
    title: str
    description: str
    incident_type: IncidentType
    priority: IncidentPriority
    flight_id: UUID | None = None
    baggage_id: UUID | None = None


@dataclass(frozen=True)
class GetIncidentsInput:
    status: IncidentStatus | None = None
    incident_type: IncidentType | None = None
    priority: IncidentPriority | None = None
    reported_by: UUID | None = None


@dataclass(frozen=True)
class IncidentOutput:
    incident_id: UUID
    reported_by: UUID
    title: str
    description: str
    incident_type: IncidentType
    priority: IncidentPriority
    status: IncidentStatus
    flight_id: UUID | None
    baggage_id: UUID | None
    created_at: datetime
    resolved_at: datetime | None
