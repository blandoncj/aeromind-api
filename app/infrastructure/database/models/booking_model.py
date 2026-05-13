from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.user_id"), index=True
    )
    flight_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("flights.flight_id"), index=True
    )
    booking_reference: Mapped[str] = mapped_column(
        String(6), unique=True, index=True)
    cabin_class: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    seat_number: Mapped[str | None] = mapped_column(String(5), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
