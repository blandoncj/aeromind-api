import pytest

from app.domain.value_objects.nationality import Nationality


class TestNationality:
    def test_valid_country_code(self) -> None:
        nat = Nationality("CO")
        assert nat.code == "CO"

    def test_normalizes_lowercase(self) -> None:
        nat = Nationality("co")
        assert nat.code == "CO"

    def test_normalizes_whitespace(self) -> None:
        nat = Nationality("  US  ")
        assert nat.code == "US"

    def test_name_property(self) -> None:
        nat = Nationality("CO")
        assert nat.name == "Colombia"

    def test_valid_us_code(self) -> None:
        nat = Nationality("US")
        assert nat.name == "United States"

    def test_raises_when_invalid_code(self) -> None:
        with pytest.raises(ValueError, match="Invalid country code"):
            Nationality("XX")

    def test_raises_when_empty(self) -> None:
        with pytest.raises(ValueError):
            Nationality("")

    def test_raises_when_three_letters(self) -> None:
        with pytest.raises(ValueError):
            Nationality("COL")

    def test_equality_by_code(self) -> None:
        assert Nationality("CO") == Nationality("co")

    def test_immutable(self) -> None:
        nat = Nationality("CO")
        with pytest.raises(Exception):
            nat.code = "US"  # type: ignore[misc]
