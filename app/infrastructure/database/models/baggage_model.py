from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class BaggageModel(Base):
    __tablename__ = "baggage"

    baggage_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True)
    booking_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("bookings.booking_id")
    )
    tag: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    baggage_type: Mapped[str] = mapped_column(String(20))
    weight_kg: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
