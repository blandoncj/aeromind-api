from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.api.dependencies import (
    get_report_lost_baggage_use_case,
    get_track_baggage_use_case,
)
from app.application.dtos.baggage_dtos import ReportLostBaggageInput, TrackBaggageInput
from app.application.use_cases.baggage.report_lost_baggage import ReportLostBaggageUseCase
from app.application.use_cases.baggage.track_baggage import TrackBaggageUseCase
from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.baggage_type import BaggageType

router = APIRouter(prefix="/baggage", tags=["baggage"])


class BaggageResponse(BaseModel):
    baggage_id: UUID
    booking_id: UUID
    tag: str
    baggage_type: BaggageType
    weight_kg: float
    status: BaggageStatus
    description: str | None


class ReportLostBaggageRequest(BaseModel):
    tag: str
    reported_by: UUID
    description: str | None = None


class ReportLostBaggageResponse(BaseModel):
    baggage_id: UUID
    tag: str
    incident_id: UUID


@router.get("/{tag}", response_model=BaggageResponse)
async def track_baggage(
    tag: str,
    use_case: Annotated[TrackBaggageUseCase, Depends(get_track_baggage_use_case)],
) -> BaggageResponse:
    result = await use_case.execute(TrackBaggageInput(tag=tag))
    return BaggageResponse(**vars(result))


@router.post(
    "/report-lost",
    response_model=ReportLostBaggageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def report_lost_baggage(
    body: ReportLostBaggageRequest,
    use_case: Annotated[ReportLostBaggageUseCase, Depends(get_report_lost_baggage_use_case)],
) -> ReportLostBaggageResponse:
    result = await use_case.execute(ReportLostBaggageInput(
        tag=body.tag,
        reported_by=body.reported_by,
        description=body.description,
    ))
    return ReportLostBaggageResponse(**vars(result))
