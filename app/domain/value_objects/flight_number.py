import re
from dataclasses import dataclass

from app.domain.exceptions.invalid_flight_number_error import (
    InvalidFlightNumberError)

# IATA format: 2-letter airline code + 1-4 digits (e.g. AA123, LA2345)
_FLIGHT_NUMBER_PATTERN = re.compile(r"^[A-Z]{2}\d{1,4}$")


@dataclass(frozen=True)
class FlightNumber:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        object.__setattr__(self, "value", normalized)
        self._validate(normalized)

    def _validate(self, value: str) -> None:
        if not _FLIGHT_NUMBER_PATTERN.fullmatch(value):
            raise InvalidFlightNumberError(
                message="""Flight number must follow IATA format: 2 uppercase
                    letters followed by 1–4 digits.""",
                context={"value": value},
            )
