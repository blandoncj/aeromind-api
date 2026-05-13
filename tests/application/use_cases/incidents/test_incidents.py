import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


from app.application.dtos.incident_dtos import (
    CreateIncidentInput,
    GetIncidentsInput,
    IncidentOutput,
)
from app.application.use_cases.incidents.create_incident import (
    CreateIncidentUseCase)
from app.application.use_cases.incidents.get_incidents import (
    GetIncidentsUseCase)
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType


def _make_incident_mock() -> MagicMock:
    incident = MagicMock()
    incident.incident_id = uuid4()
    incident.reported_by = uuid4()
    incident.title = "Lost baggage at BOG"
    incident.description = "Passenger reports missing bag."
    incident.incident_type = IncidentType.LOST_BAGGAGE
    incident.priority = IncidentPriority.HIGH
    incident.status = IncidentStatus.OPEN
    incident.flight_id = None
    incident.baggage_id = uuid4()
    incident.created_at = datetime(2026, 5, 12, tzinfo=timezone.utc)
    incident.resolved_at = None
    return incident


class TestCreateIncidentUseCase:
    def test_returns_incident_output(self) -> None:
        repo = AsyncMock()
        repo.save.return_value = None
        input = CreateIncidentInput(
            reported_by=uuid4(),
            title="Lost baggage at BOG",
            description="Passenger reports missing bag.",
            incident_type=IncidentType.LOST_BAGGAGE,
            priority=IncidentPriority.HIGH,
        )

        result = asyncio.run(CreateIncidentUseCase(repo).execute(input))

        assert isinstance(result, IncidentOutput)
        assert result.title == "Lost baggage at BOG"
        assert result.incident_type == IncidentType.LOST_BAGGAGE
        assert result.priority == IncidentPriority.HIGH
        assert result.status == IncidentStatus.OPEN
        assert result.incident_id is not None

    def test_saves_incident_to_repository(self) -> None:
        repo = AsyncMock()
        input = CreateIncidentInput(
            reported_by=uuid4(),
            title="Flight delay report",
            description="Flight AV123 delayed 3 hours.",
            incident_type=IncidentType.FLIGHT_DELAY,
            priority=IncidentPriority.MEDIUM,
        )

        asyncio.run(CreateIncidentUseCase(repo).execute(input))

        repo.save.assert_called_once()

    def test_links_flight_id_when_provided(self) -> None:
        repo = AsyncMock()
        flight_id = uuid4()
        input = CreateIncidentInput(
            reported_by=uuid4(),
            title="Flight delay",
            description="Delayed.",
            incident_type=IncidentType.FLIGHT_DELAY,
            priority=IncidentPriority.LOW,
            flight_id=flight_id,
        )

        result = asyncio.run(CreateIncidentUseCase(repo).execute(input))

        assert result.flight_id == flight_id


class TestGetIncidentsUseCase:
    def test_returns_all_incidents_without_filters(self) -> None:
        repo = AsyncMock()
        repo.find_all.return_value = [
            _make_incident_mock(), _make_incident_mock()]

        result = asyncio.run(GetIncidentsUseCase(
            repo).execute(GetIncidentsInput()))

        assert len(result) == 2
        assert all(isinstance(i, IncidentOutput) for i in result)

    def test_passes_filters_to_repository(self) -> None:
        repo = AsyncMock()
        repo.find_all.return_value = []

        asyncio.run(
            GetIncidentsUseCase(repo).execute(
                GetIncidentsInput(
                    status=IncidentStatus.OPEN,
                    incident_type=IncidentType.LOST_BAGGAGE,
                    priority=IncidentPriority.HIGH,
                )
            )
        )

        repo.find_all.assert_called_once_with(
            status=IncidentStatus.OPEN,
            incident_type=IncidentType.LOST_BAGGAGE,
            priority=IncidentPriority.HIGH,
            reported_by=None,
        )

    def test_returns_empty_list_when_no_incidents(self) -> None:
        repo = AsyncMock()
        repo.find_all.return_value = []

        result = asyncio.run(GetIncidentsUseCase(
            repo).execute(GetIncidentsInput()))

        assert result == []
