import re
from dataclasses import dataclass

from app.domain.exceptions.invalid_booking_reference_error import (
    InvalidBookingReferenceError,
)

# PNR format: exactly 6 alphanumeric uppercase characters (e.g. ABC123, XY12Z9)
_PNR_PATTERN = re.compile(r"^[A-Z0-9]{6}$")


@dataclass(frozen=True)
class BookingReference:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        object.__setattr__(self, "value", normalized)
        self._validate(normalized)

    def _validate(self, value: str) -> None:
        if not _PNR_PATTERN.fullmatch(value):
            raise InvalidBookingReferenceError(
                message="""Booking reference must be exactly 6 alphanumeric 
                characters (PNR format).""",
                context={"value": value},
            )
