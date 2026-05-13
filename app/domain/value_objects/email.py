import re
from dataclasses import dataclass

from app.domain.exceptions.invalid_email_error import InvalidEmailError

_EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)
_MAX_LENGTH = 254


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        object.__setattr__(self, "value", normalized)
        self._validate(normalized)

    def _validate(self, value: str) -> None:
        if len(value) > _MAX_LENGTH:
            raise InvalidEmailError(
                message=f"Email must not exceed {_MAX_LENGTH} characters.",
                context={"value": value, "lenght": len(
                    value), "max_length": _MAX_LENGTH}
            )

        if not _EMAIL_PATTERN.fullmatch(value):
            raise InvalidEmailError(
                message="Email format is invalid.",
                context={"value": value}
            )
