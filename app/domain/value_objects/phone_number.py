from dataclasses import dataclass

import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat

from app.domain.exceptions.invalid_phone_number_error import (
    InvalidPhoneNumberError
)


@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __post_init__(self) -> None:
        normalized = self._parse_and_normalize(self.value.strip())
        object.__setattr__(self, "value", normalized)

    def _parse_and_normalize(self, raw: str) -> str:
        try:
            parsed = phonenumbers.parse(raw, None)
        except NumberParseException:
            raise InvalidPhoneNumberError(
                message="""
                    Phone number could not be parsed. Include country code
                    (e.g +57)
                """
            )

        if not phonenumbers.is_valid_number(parsed):
            raise InvalidPhoneNumberError(
                message="Phone number is not valid.",
                context={"value": raw}
            )

        return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
