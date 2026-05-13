from app.application.dtos.baggage_dtos import BaggageOutput, TrackBaggageInput
from app.application.exceptions.baggage_not_found_error import (
    BaggageNotFoundError)
from app.application.ports.baggage_repository import BaggageRepository
from app.domain.value_objects.baggage_tag import BaggageTag


class TrackBaggageUseCase:
    def __init__(self, baggage_repository: BaggageRepository) -> None:
        self._baggage_repository = baggage_repository

    async def execute(self, input: TrackBaggageInput) -> BaggageOutput:
        tag = BaggageTag(input.tag)
        baggage = await self._baggage_repository.find_by_tag(tag)
        if baggage is None:
            raise BaggageNotFoundError(tag.value)
        return BaggageOutput(
            baggage_id=baggage.baggage_id,
            booking_id=baggage.booking_id,
            tag=baggage.tag.value,
            baggage_type=baggage.baggage_type,
            weight_kg=baggage.weight_kg,
            status=baggage.status,
            description=baggage.description,
        )
