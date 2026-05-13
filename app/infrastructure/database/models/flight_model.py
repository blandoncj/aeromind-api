from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class FlightModel(Base):
    __tablename__ = "flights"

    flight_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(10), index=True)
    origin: Mapped[str] = mapped_column(String(3))
    destination: Mapped[str] = mapped_column(String(3))
    scheduled_departure: Mapped[datetime] = mapped_column(DateTime)
    scheduled_arrival: Mapped[datetime] = mapped_column(DateTime)
    airline: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20))
    gate: Mapped[str | None] = mapped_column(String(10), nullable=True)
    aircraft_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True)
    actual_departure: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)
    actual_arrival: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
