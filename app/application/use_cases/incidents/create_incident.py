from app.application.dtos.incident_dtos import (
    CreateIncidentInput, IncidentOutput)
from app.application.ports.incident_repository import IncidentRepository
from app.domain.entities.incident import Incident


class CreateIncidentUseCase:
    def __init__(self, incident_repository: IncidentRepository) -> None:
        self._incident_repository = incident_repository

    async def execute(self, input: CreateIncidentInput) -> IncidentOutput:
        incident = Incident(
            reported_by=input.reported_by,
            title=input.title,
            description=input.description,
            incident_type=input.incident_type,
            priority=input.priority,
            flight_id=input.flight_id,
            baggage_id=input.baggage_id,
        )
        await self._incident_repository.save(incident)
        return IncidentOutput(
            incident_id=incident.incident_id,
            reported_by=incident.reported_by,
            title=incident.title,
            description=incident.description,
            incident_type=incident.incident_type,
            priority=incident.priority,
            status=incident.status,
            flight_id=incident.flight_id,
            baggage_id=incident.baggage_id,
            created_at=incident.created_at,
            resolved_at=incident.resolved_at,
        )
