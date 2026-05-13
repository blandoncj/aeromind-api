from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from pydantic import BaseModel

from app.api.dependencies import (
    get_create_incident_use_case,
    get_get_incidents_use_case,
)
from app.application.dtos.incident_dtos import CreateIncidentInput, GetIncidentsInput
from app.application.use_cases.incidents.create_incident import CreateIncidentUseCase
from app.application.use_cases.incidents.get_incidents import GetIncidentsUseCase
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType

router = APIRouter(prefix="/incidents", tags=["incidents"])


class IncidentResponse(BaseModel):
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


class CreateIncidentRequest(BaseModel):
    reported_by: UUID
    title: str
    description: str
    incident_type: IncidentType
    priority: IncidentPriority
    flight_id: UUID | None = None
    baggage_id: UUID | None = None


@router.post("", status_code=http_status.HTTP_201_CREATED)
async def create_incident(
    body: CreateIncidentRequest,
    use_case: Annotated[CreateIncidentUseCase, Depends(get_create_incident_use_case)],
) -> IncidentResponse:
    result = await use_case.execute(CreateIncidentInput(
        reported_by=body.reported_by,
        title=body.title,
        description=body.description,
        incident_type=body.incident_type,
        priority=body.priority,
        flight_id=body.flight_id,
        baggage_id=body.baggage_id,
    ))
    return IncidentResponse(**vars(result))


@router.get("")
async def get_incidents(
    use_case: Annotated[GetIncidentsUseCase, Depends(get_get_incidents_use_case)],
    incident_status: IncidentStatus | None = None,
    incident_type: IncidentType | None = None,
    priority: IncidentPriority | None = None,
    reported_by: UUID | None = None,
) -> list[IncidentResponse]:
    results = await use_case.execute(GetIncidentsInput(
        status=incident_status,
        incident_type=incident_type,
        priority=priority,
        reported_by=reported_by,
    ))
    return [IncidentResponse(**vars(i)) for i in results]
