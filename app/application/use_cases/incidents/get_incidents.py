from app.application.dtos.incident_dtos import (
    GetIncidentsInput, IncidentOutput)
from app.application.ports.incident_repository import IncidentRepository


class GetIncidentsUseCase:
    def __init__(self, incident_repository: IncidentRepository) -> None:
        self._incident_repository = incident_repository

    async def execute(self, input: GetIncidentsInput) -> list[IncidentOutput]:
        incidents = await self._incident_repository.find_all(
            status=input.status,
            incident_type=input.incident_type,
            priority=input.priority,
            reported_by=input.reported_by,
        )
        return [
            IncidentOutput(
                incident_id=i.incident_id,
                reported_by=i.reported_by,
                title=i.title,
                description=i.description,
                incident_type=i.incident_type,
                priority=i.priority,
                status=i.status,
                flight_id=i.flight_id,
                baggage_id=i.baggage_id,
                created_at=i.created_at,
                resolved_at=i.resolved_at,
            )
            for i in incidents
        ]
