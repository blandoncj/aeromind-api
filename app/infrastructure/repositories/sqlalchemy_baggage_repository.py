from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.baggage_repository import BaggageRepository
from app.domain.entities.baggage import Baggage
from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.baggage_type import BaggageType
from app.domain.value_objects.baggage_tag import BaggageTag
from app.infrastructure.database.models.baggage_model import BaggageModel


class SqlAlchemyBaggageRepository(BaggageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_tag(self, tag: BaggageTag) -> Baggage | None:
        result = await self._session.execute(
            select(BaggageModel).where(BaggageModel.tag == tag.value)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, baggage: Baggage) -> None:
        model = await self._session.get(BaggageModel, baggage.baggage_id)
        if model is None:
            self._session.add(self._to_model(baggage))
        else:
            self._update_model(model, baggage)
        await self._session.flush()

    def _to_entity(self, model: BaggageModel) -> Baggage:
        return Baggage(
            baggage_id=model.baggage_id,
            booking_id=model.booking_id,
            tag=BaggageTag(value=model.tag),
            baggage_type=BaggageType(model.baggage_type),
            weight_kg=model.weight_kg,
            status=BaggageStatus(model.status),
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, baggage: Baggage) -> BaggageModel:
        return BaggageModel(
            baggage_id=baggage.baggage_id,
            booking_id=baggage.booking_id,
            tag=baggage.tag.value,
            baggage_type=baggage.baggage_type.value,
            weight_kg=baggage.weight_kg,
            status=baggage.status.value,
            description=baggage.description,
            created_at=baggage.created_at,
            updated_at=baggage.updated_at,
        )

    def _update_model(self, model: BaggageModel, baggage: Baggage) -> None:
        model.status = baggage.status.value
        model.description = baggage.description
        model.updated_at = baggage.updated_at
