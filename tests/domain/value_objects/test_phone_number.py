import pytest

from app.domain.exceptions.invalid_phone_number_error import InvalidPhoneNumberError
from app.domain.value_objects.phone_number import PhoneNumber


class TestPhoneNumber:
    def test_valid_colombian_number(self) -> None:
        phone = PhoneNumber("+573001234567")
        assert phone.value == "+573001234567"

    def test_valid_us_number(self) -> None:
        phone = PhoneNumber("+12125550100")
        assert phone.value == "+12125550100"

    def test_normalizes_to_e164(self) -> None:
        phone = PhoneNumber("+57 300 123 4567")
        assert phone.value == "+573001234567"

    def test_normalizes_whitespace(self) -> None:
        phone = PhoneNumber("  +573001234567  ")
        assert phone.value == "+573001234567"

    def test_raises_when_no_country_code(self) -> None:
        with pytest.raises(InvalidPhoneNumberError) as exc_info:
            PhoneNumber("3001234567")
        assert exc_info.value.code == "INVALID_PHONE_NUMBER"

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidPhoneNumberError):
            PhoneNumber("")

    def test_raises_when_invalid_number(self) -> None:
        with pytest.raises(InvalidPhoneNumberError):
            PhoneNumber("+57000")

    def test_equality_by_value(self) -> None:
        assert PhoneNumber("+573001234567") == PhoneNumber("+57 300 123 4567")

    def test_immutable(self) -> None:
        phone = PhoneNumber("+573001234567")
        with pytest.raises(Exception):
            phone.value = "+573009999999"  # type: ignore[misc]
