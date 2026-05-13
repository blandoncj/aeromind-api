from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class IncidentModel(Base):
    __tablename__ = "incidents"

    incident_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True)
    reported_by: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.user_id"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    incident_type: Mapped[str] = mapped_column(String(30))
    priority: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    flight_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("flights.flight_id"), nullable=True
    )
    baggage_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("baggage.baggage_id"), nullable=True
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
