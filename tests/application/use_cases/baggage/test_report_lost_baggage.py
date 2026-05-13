import asyncio
from unittest.mock import AsyncMock, MagicMock, call
from uuid import uuid4

import pytest

from app.application.dtos.baggage_dtos import ReportLostBaggageInput, ReportLostBaggageOutput
from app.application.exceptions.baggage_not_found_error import BaggageNotFoundError
from app.application.use_cases.baggage.report_lost_baggage import ReportLostBaggageUseCase
from app.domain.enums.baggage_status import BaggageStatus
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_type import IncidentType


def _make_baggage(tag: str = "0014123456") -> MagicMock:
    baggage = MagicMock()
    baggage.baggage_id = uuid4()
    baggage.tag.value = tag
    baggage.status = BaggageStatus.IN_TRANSIT
    return baggage


def _make_use_case(baggage=None) -> tuple[ReportLostBaggageUseCase, AsyncMock, AsyncMock]:
    baggage_repo = AsyncMock()
    baggage_repo.find_by_tag.return_value = baggage
    baggage_repo.save.return_value = None

    incident_repo = AsyncMock()
    incident_repo.save.return_value = None

    return ReportLostBaggageUseCase(baggage_repo, incident_repo), baggage_repo, incident_repo


class TestReportLostBaggageUseCase:
    def test_returns_output_with_baggage_and_incident_ids(self) -> None:
        baggage = _make_baggage()
        use_case, _, _ = _make_use_case(baggage)

        result = asyncio.run(
            use_case.execute(ReportLostBaggageInput(tag="0014123456", reported_by=uuid4()))
        )

        assert isinstance(result, ReportLostBaggageOutput)
        assert result.baggage_id == baggage.baggage_id
        assert result.tag == "0014123456"
        assert result.incident_id is not None

    def test_raises_when_baggage_not_found(self) -> None:
        use_case, _, _ = _make_use_case(baggage=None)

        with pytest.raises(BaggageNotFoundError):
            asyncio.run(
                use_case.execute(ReportLostBaggageInput(tag="0014123456", reported_by=uuid4()))
            )

    def test_marks_baggage_status_as_missing(self) -> None:
        baggage = _make_baggage()
        use_case, baggage_repo, _ = _make_use_case(baggage)

        asyncio.run(use_case.execute(ReportLostBaggageInput(tag="0014123456", reported_by=uuid4())))

        assert baggage.status == BaggageStatus.MISSING
        baggage_repo.save.assert_called_once_with(baggage)

    def test_creates_incident_with_correct_type_and_priority(self) -> None:
        use_case, _, incident_repo = _make_use_case(_make_baggage())

        asyncio.run(use_case.execute(ReportLostBaggageInput(tag="0014123456", reported_by=uuid4())))

        saved_incident = incident_repo.save.call_args[0][0]
        assert saved_incident.incident_type == IncidentType.LOST_BAGGAGE
        assert saved_incident.priority == IncidentPriority.HIGH

    def test_does_not_create_incident_when_baggage_not_found(self) -> None:
        use_case, _, incident_repo = _make_use_case(baggage=None)

        with pytest.raises(BaggageNotFoundError):
            asyncio.run(
                use_case.execute(ReportLostBaggageInput(tag="0014123456", reported_by=uuid4()))
            )

        incident_repo.save.assert_not_called()

    def test_uses_provided_description_in_incident(self) -> None:
        use_case, _, incident_repo = _make_use_case(_make_baggage())

        asyncio.run(
            use_case.execute(
                ReportLostBaggageInput(
                    tag="0014123456", reported_by=uuid4(), description="Left at gate B3"
                )
            )
        )

        saved_incident = incident_repo.save.call_args[0][0]
        assert saved_incident.description == "Left at gate B3"
