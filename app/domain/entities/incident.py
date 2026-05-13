from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType


@dataclass
class Incident:
    reported_by: UUID
    title: str
    description: str
    incident_type: IncidentType
    priority: IncidentPriority
    status: IncidentStatus = IncidentStatus.OPEN
    flight_id: UUID | None = None
    baggage_id: UUID | None = None
    resolved_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    incident_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Title must not be empty.")
        if not self.description.strip():
            raise ValueError("Description must not be empty.")
