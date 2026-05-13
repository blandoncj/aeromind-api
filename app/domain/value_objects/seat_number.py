import re
from dataclasses import dataclass

from app.domain.exceptions.invalid_seat_number_error import InvalidSeatNumberError

# Seat format: row 1-99 + letter A-F (e.g. 1A, 12C, 34F)
_SEAT_PATTERN = re.compile(r"^([1-9]|[1-9][0-9])[A-F]$")


@dataclass(frozen=True)
class SeatNumber:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        object.__setattr__(self, "value", normalized)
        self._validate(normalized)

    def _validate(self, value: str) -> None:
        if not _SEAT_PATTERN.fullmatch(value):
            raise InvalidSeatNumberError(
                message="Seat number must be a row (1–99) followed by a letter A–F (e.g. 12A).",
                context={"value": value},
            )
