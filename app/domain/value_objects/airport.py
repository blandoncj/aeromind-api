import re
from dataclasses import dataclass

from app.domain.exceptions.invalid_airport_code_error import (
    InvalidAirportCodeError)

# IATA airport code: exactly 3 uppercase letters (e.g. BOG, MIA, JFK)
_IATA_CODE_PATTERN = re.compile(r"^[A-Z]{3}$")


@dataclass(frozen=True)
class Airport:
    code: str

    def __post_init__(self) -> None:
        normalized = self.code.strip().upper()
        object.__setattr__(self, "code", normalized)
        self._validate(normalized)

    def _validate(self, value: str) -> None:
        if not _IATA_CODE_PATTERN.fullmatch(value):
            raise InvalidAirportCodeError(
                message="""
                    Airport code must be exactly 3 uppercase letters
                    (IATA format).""",
                context={"code": value},
            )
