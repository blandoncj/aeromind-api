import pytest
from uuid import uuid4

from app.domain.entities.baggage import Baggage
from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.baggage_type import BaggageType
from app.domain.value_objects.baggage_tag import BaggageTag


_BOOKING_ID = uuid4()
_TAG = BaggageTag("0014123456")


def _make_baggage(**overrides) -> Baggage:  # type: ignore[no-untyped-def]
    defaults = dict(
        booking_id=_BOOKING_ID,
        tag=_TAG,
        baggage_type=BaggageType.CHECKED,
        weight_kg=23.0,
    )
    defaults.update(overrides)
    return Baggage(**defaults)


class TestBaggage:
    def test_creates_baggage_with_defaults(self) -> None:
        baggage = _make_baggage()
        assert baggage.status == BaggageStatus.CHECKED_IN
        assert baggage.description is None

    def test_baggage_id_is_assigned(self) -> None:
        baggage = _make_baggage()
        assert baggage.baggage_id is not None

    def test_two_baggages_have_different_ids(self) -> None:
        assert _make_baggage().baggage_id != _make_baggage().baggage_id

    def test_creates_baggage_with_description(self) -> None:
        baggage = _make_baggage(description="Maleta negra grande")
        assert baggage.description == "Maleta negra grande"

    def test_creates_baggage_with_carry_on_type(self) -> None:
        baggage = _make_baggage(baggage_type=BaggageType.CARRY_ON, weight_kg=8.0)
        assert baggage.baggage_type == BaggageType.CARRY_ON

    def test_creates_baggage_with_missing_status(self) -> None:
        baggage = _make_baggage(status=BaggageStatus.MISSING)
        assert baggage.status == BaggageStatus.MISSING

    def test_references_booking_by_id(self) -> None:
        baggage = _make_baggage()
        assert baggage.booking_id == _BOOKING_ID

    def test_raises_when_weight_is_zero(self) -> None:
        with pytest.raises(ValueError, match="Weight must be greater than zero"):
            _make_baggage(weight_kg=0)

    def test_raises_when_weight_is_negative(self) -> None:
        with pytest.raises(ValueError, match="Weight must be greater than zero"):
            _make_baggage(weight_kg=-5.0)
