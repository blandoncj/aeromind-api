import pytest

from app.domain.exceptions.invalid_baggage_tag_error import InvalidBaggageTagError
from app.domain.value_objects.baggage_tag import BaggageTag


class TestBaggageTag:
    def test_valid_tag(self) -> None:
        tag = BaggageTag("0014123456")
        assert tag.value == "0014123456"

    def test_normalizes_whitespace(self) -> None:
        tag = BaggageTag("  0014123456  ")
        assert tag.value == "0014123456"

    def test_raises_when_nine_digits(self) -> None:
        with pytest.raises(InvalidBaggageTagError) as exc_info:
            BaggageTag("001412345")
        assert exc_info.value.code == "INVALID_BAGGAGE_TAG"

    def test_raises_when_eleven_digits(self) -> None:
        with pytest.raises(InvalidBaggageTagError):
            BaggageTag("00141234567")

    def test_raises_when_contains_letter(self) -> None:
        with pytest.raises(InvalidBaggageTagError):
            BaggageTag("001412345A")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(InvalidBaggageTagError):
            BaggageTag("")

    def test_equality_by_value(self) -> None:
        assert BaggageTag("0014123456") == BaggageTag("0014123456")

    def test_different_tags_not_equal(self) -> None:
        assert BaggageTag("0014123456") != BaggageTag("0014123457")

    def test_immutable(self) -> None:
        tag = BaggageTag("0014123456")
        with pytest.raises(Exception):
            tag.value = "0014123457"  # type: ignore[misc]
