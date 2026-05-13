import pytest
from datetime import date

from app.domain.exceptions.invalid_date_of_birth_error import InvalidDateOfBirthError
from app.domain.value_objects.date_of_birth import DateOfBirth


class TestDateOfBirth:
    def test_valid_date_of_birth(self) -> None:
        dob = DateOfBirth(date(1994, 6, 15))
        assert dob.value == date(1994, 6, 15)

    def test_raises_when_today(self) -> None:
        with pytest.raises(InvalidDateOfBirthError) as exc_info:
            DateOfBirth(date.today())
        assert exc_info.value.code == "INVALID_DATE_OF_BIRTH"

    def test_raises_when_future_date(self) -> None:
        with pytest.raises(InvalidDateOfBirthError):
            DateOfBirth(date(2099, 1, 1))

    def test_raises_when_before_1900(self) -> None:
        with pytest.raises(InvalidDateOfBirthError):
            DateOfBirth(date(1899, 12, 31))

    def test_boundary_year_1900_is_valid(self) -> None:
        dob = DateOfBirth(date(1900, 1, 1))
        assert dob.value.year == 1900

    def test_age_is_calculated(self) -> None:
        dob = DateOfBirth(date(1994, 1, 1))
        assert dob.age >= 30

    def test_is_minor_false_for_adult(self) -> None:
        dob = DateOfBirth(date(1994, 1, 1))
        assert dob.is_minor is False

    def test_is_minor_true_for_child(self) -> None:
        today = date.today()
        child_dob = date(today.year - 10, today.month, today.day)
        # Go back one day to avoid same-day edge case
        child_dob = date(child_dob.year, child_dob.month, max(child_dob.day - 1, 1))
        dob = DateOfBirth(child_dob)
        assert dob.is_minor is True

    def test_immutable(self) -> None:
        dob = DateOfBirth(date(1994, 6, 15))
        with pytest.raises(Exception):
            dob.value = date(2000, 1, 1)  # type: ignore[misc]
