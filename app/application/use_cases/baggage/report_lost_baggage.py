from app.application.dtos.baggage_dtos import (
    ReportLostBaggageInput, ReportLostBaggageOutput)
from app.application.exceptions.baggage_not_found_error import (
    BaggageNotFoundError)
from app.application.ports.baggage_repository import BaggageRepository
from app.application.ports.incident_repository import IncidentRepository
from app.domain.entities.incident import Incident
from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_type import IncidentType
from app.domain.value_objects.baggage_tag import BaggageTag


class ReportLostBaggageUseCase:
    def __init__(
        self,
        baggage_repository: BaggageRepository,
        incident_repository: IncidentRepository,
    ) -> None:
        self._baggage_repository = baggage_repository
        self._incident_repository = incident_repository

    async def execute(
            self, input: ReportLostBaggageInput) -> ReportLostBaggageOutput:
        tag = BaggageTag(input.tag)
        baggage = await self._baggage_repository.find_by_tag(tag)
        if baggage is None:
            raise BaggageNotFoundError(tag.value)

        baggage.status = BaggageStatus.MISSING
        await self._baggage_repository.save(baggage)

        incident = Incident(
            reported_by=input.reported_by,
            title=f"Lost baggage: {tag.value}",
            description=input.description or f"Baggage with tag {
                tag.value} reported as lost.",
            incident_type=IncidentType.LOST_BAGGAGE,
            priority=IncidentPriority.HIGH,
            baggage_id=baggage.baggage_id,
        )
        await self._incident_repository.save(incident)

        return ReportLostBaggageOutput(
            baggage_id=baggage.baggage_id,
            tag=tag.value,
            incident_id=incident.incident_id,
        )
