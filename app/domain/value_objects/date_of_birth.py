from dataclasses import dataclass
from datetime import date

from app.domain.exceptions.invalid_date_of_birth_error import (
    InvalidDateOfBirthError
)


@dataclass(frozen=True)
class DateOfBirth:
    value: date

    def __post_init__(self) -> None:
        today = date.today()

        if self.value >= today:
            raise InvalidDateOfBirthError(
                message="Date of birth must be in the past.",
                context={"value": self.value.isoformat(),
                         "today": today.isoformat()}
            )

        if self.value.year < 1900:
            raise InvalidDateOfBirthError(
                message="Date of birth must be after January 1, 1900.",
                context={"value": self.value.isoformat()}
            )

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.value.year - (
            (today.month, today.day) < (self.value.month, self.value.day)
        )

    @property
    def is_minor(self) -> bool:
        return self.age < 18
