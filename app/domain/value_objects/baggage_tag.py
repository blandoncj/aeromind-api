import re
from dataclasses import dataclass

from app.domain.exceptions.invalid_baggage_tag_error import (
    InvalidBaggageTagError)

# IATA baggage license plate: exactly 10 digits (e.g. 0014123456)
_TAG_PATTERN = re.compile(r"^\d{10}$")


@dataclass(frozen=True)
class BaggageTag:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        object.__setattr__(self, "value", normalized)
        self._validate(normalized)

    def _validate(self, value: str) -> None:
        if not _TAG_PATTERN.fullmatch(value):
            raise InvalidBaggageTagError(
                message="""Baggage tag must be exactly 10 digits
                (IATA license plate format).""",
                context={"value": value},
            )
