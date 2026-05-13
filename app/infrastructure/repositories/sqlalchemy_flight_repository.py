from datetime import date
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.flight_repository import FlightRepository
from app.domain.entities.flight import Flight
from app.domain.enums.flight_status import FlightStatus
from app.domain.value_objects.airport import Airport
from app.domain.value_objects.flight_number import FlightNumber
from app.infrastructure.database.models.flight_model import FlightModel


class SqlAlchemyFlightRepository(FlightRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, flight_id: UUID) -> Flight | None:
        model = await self._session.get(FlightModel, flight_id)
        return self._to_entity(model) if model else None

    async def search(
        self,
        origin: Airport,
        destination: Airport,
        departure_date: date,
    ) -> list[Flight]:
        result = await self._session.execute(
            select(FlightModel).where(
                FlightModel.origin == origin.code,
                FlightModel.destination == destination.code,
                func.date(FlightModel.scheduled_departure) == departure_date,
            )
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    def _to_entity(self, model: FlightModel) -> Flight:
        return Flight(
            flight_id=model.flight_id,
            flight_number=FlightNumber(value=model.flight_number),
            origin=Airport(code=model.origin),
            destination=Airport(code=model.destination),
            scheduled_departure=model.scheduled_departure,
            scheduled_arrival=model.scheduled_arrival,
            airline=model.airline,
            status=FlightStatus(model.status),
            gate=model.gate,
            aircraft_type=model.aircraft_type,
            actual_departure=model.actual_departure,
            actual_arrival=model.actual_arrival,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
