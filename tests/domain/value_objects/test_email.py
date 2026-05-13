import pytest

from app.domain.exceptions.invalid_email_error import InvalidEmailError
from app.domain.value_objects.email import Email


class TestEmail:
    def test_valid_email(self) -> None:
        email = Email("user@example.com")
        assert email.value == "user@example.com"

    def test_normalizes_uppercase(self) -> None:
        email = Email("USER@EXAMPLE.COM")
        assert email.value == "user@example.com"

    def test_normalizes_whitespace(self) -> None:
        email = Email("  user@example.com  ")
        assert email.value == "user@example.com"

    def test_valid_with_subdomain(self) -> None:
        email = Email("user@mail.example.co")
        assert email.value == "user@mail.example.co"

    def test_valid_with_plus(self) -> None:
        email = Email("user+tag@example.com")
        assert email.value == "user+tag@example.com"

    def test_raises_when_missing_at(self) -> None:
        with pytest.raises(InvalidEmailError) as exc_info:
            Email("userexample.com")
        assert exc_info.value.code == "INVALID_EMAIL"

    def test_raises_when_missing_domain(self) -> None:
        with pytest.raises(InvalidEmailError):
            Email("user@")

    def test_raises_when_missing_tld(self) -> None:
        with pytest.raises(InvalidEmailError):
            Email("user@example")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidEmailError):
            Email("")

    def test_raises_when_exceeds_max_length(self) -> None:
        long_email = "a" * 245 + "@example.com"
        with pytest.raises(InvalidEmailError):
            Email(long_email)

    def test_equality_by_value(self) -> None:
        assert Email("User@Example.COM") == Email("user@example.com")

    def test_immutable(self) -> None:
        email = Email("user@example.com")
        with pytest.raises(Exception):
            email.value = "other@example.com"  # type: ignore[misc]
