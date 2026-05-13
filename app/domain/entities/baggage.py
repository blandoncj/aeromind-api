from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.baggage_type import BaggageType
from app.domain.value_objects.baggage_tag import BaggageTag


@dataclass
class Baggage:
    booking_id: UUID
    tag: BaggageTag
    baggage_type: BaggageType
    weight_kg: float
    status: BaggageStatus = BaggageStatus.CHECKED_IN
    description: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    baggage_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.weight_kg <= 0:
            raise ValueError("Weight must be greater than zero.")
