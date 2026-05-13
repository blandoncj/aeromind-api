from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.incident_repository import IncidentRepository
from app.domain.entities.incident import Incident
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType
from app.infrastructure.database.models.incident_model import IncidentModel


class SqlAlchemyIncidentRepository(IncidentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, incident: Incident) -> None:
        model = await self._session.get(IncidentModel, incident.incident_id)
        if model is None:
            self._session.add(self._to_model(incident))
        else:
            self._update_model(model, incident)
        await self._session.flush()

    async def find_all(
        self,
        *,
        status: IncidentStatus | None = None,
        incident_type: IncidentType | None = None,
        priority: IncidentPriority | None = None,
        reported_by: UUID | None = None,
    ) -> list[Incident]:
        query = select(IncidentModel)
        if status is not None:
            query = query.where(IncidentModel.status == status.value)
        if incident_type is not None:
            query = query.where(
                IncidentModel.incident_type == incident_type.value)
        if priority is not None:
            query = query.where(IncidentModel.priority == priority.value)
        if reported_by is not None:
            query = query.where(IncidentModel.reported_by == reported_by)

        result = await self._session.execute(query)
        return [self._to_entity(m) for m in result.scalars().all()]

    def _to_entity(self, model: IncidentModel) -> Incident:
        return Incident(
            incident_id=model.incident_id,
            reported_by=model.reported_by,
            title=model.title,
            description=model.description,
            incident_type=IncidentType(model.incident_type),
            priority=IncidentPriority(model.priority),
            status=IncidentStatus(model.status),
            flight_id=model.flight_id,
            baggage_id=model.baggage_id,
            resolved_at=model.resolved_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, incident: Incident) -> IncidentModel:
        return IncidentModel(
            incident_id=incident.incident_id,
            reported_by=incident.reported_by,
            title=incident.title,
            description=incident.description,
            incident_type=incident.incident_type.value,
            priority=incident.priority.value,
            status=incident.status.value,
            flight_id=incident.flight_id,
            baggage_id=incident.baggage_id,
            resolved_at=incident.resolved_at,
            created_at=incident.created_at,
            updated_at=incident.updated_at,
        )

    def _update_model(self, model: IncidentModel, incident: Incident) -> None:
        model.title = incident.title
        model.description = incident.description
        model.incident_type = incident.incident_type.value
        model.priority = incident.priority.value
        model.status = incident.status.value
        model.flight_id = incident.flight_id
        model.baggage_id = incident.baggage_id
        model.resolved_at = incident.resolved_at
        model.updated_at = incident.updated_at
