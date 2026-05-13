import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dtos.baggage_dtos import BaggageOutput, TrackBaggageInput
from app.application.exceptions.baggage_not_found_error import BaggageNotFoundError
from app.application.use_cases.baggage.track_baggage import TrackBaggageUseCase
from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.baggage_type import BaggageType


def _make_baggage(tag: str = "0014123456") -> MagicMock:
    baggage = MagicMock()
    baggage.baggage_id = uuid4()
    baggage.booking_id = uuid4()
    baggage.tag.value = tag
    baggage.baggage_type = BaggageType.CHECKED
    baggage.weight_kg = 23.5
    baggage.status = BaggageStatus.IN_TRANSIT
    baggage.description = None
    return baggage


class TestTrackBaggageUseCase:
    def test_returns_baggage_output(self) -> None:
        baggage = _make_baggage()
        repo = AsyncMock()
        repo.find_by_tag.return_value = baggage

        result = asyncio.run(TrackBaggageUseCase(repo).execute(TrackBaggageInput("0014123456")))

        assert isinstance(result, BaggageOutput)
        assert result.tag == "0014123456"
        assert result.status == BaggageStatus.IN_TRANSIT
        assert result.weight_kg == pytest.approx(23.5)

    def test_raises_when_baggage_not_found(self) -> None:
        repo = AsyncMock()
        repo.find_by_tag.return_value = None

        with pytest.raises(BaggageNotFoundError) as exc_info:
            asyncio.run(TrackBaggageUseCase(repo).execute(TrackBaggageInput("0014123456")))

        assert exc_info.value.code == "BAGGAGE_NOT_FOUND"

    def test_queries_repository_with_tag_value_object(self) -> None:
        from app.domain.value_objects.baggage_tag import BaggageTag

        repo = AsyncMock()
        repo.find_by_tag.return_value = _make_baggage()

        asyncio.run(TrackBaggageUseCase(repo).execute(TrackBaggageInput("0014123456")))

        called_tag = repo.find_by_tag.call_args[0][0]
        assert isinstance(called_tag, BaggageTag)
        assert called_tag.value == "0014123456"
