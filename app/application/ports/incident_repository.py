from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.incident import Incident
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType


class IncidentRepository(ABC):
    @abstractmethod
    async def save(self, incident: Incident) -> None: ...

    @abstractmethod
    async def find_all(
        self,
        *,
        status: IncidentStatus | None = None,
        incident_type: IncidentType | None = None,
        priority: IncidentPriority | None = None,
        reported_by: UUID | None = None,
    ) -> list[Incident]: ...
