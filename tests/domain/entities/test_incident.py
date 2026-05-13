import pytest
from uuid import uuid4

from app.domain.entities.incident import Incident
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType


_USER_ID = uuid4()
_FLIGHT_ID = uuid4()
_BAGGAGE_ID = uuid4()


def _make_incident(**overrides) -> Incident:  # type: ignore[no-untyped-def]
    defaults = dict(
        reported_by=_USER_ID,
        title="Maleta no llegó al destino",
        description="El pasajero reporta que su equipaje no apareció en la cinta.",
        incident_type=IncidentType.LOST_BAGGAGE,
        priority=IncidentPriority.HIGH,
    )
    defaults.update(overrides)
    return Incident(**defaults)


class TestIncident:
    def test_creates_incident_with_defaults(self) -> None:
        incident = _make_incident()
        assert incident.status == IncidentStatus.OPEN
        assert incident.flight_id is None
        assert incident.baggage_id is None
        assert incident.resolved_at is None

    def test_incident_id_is_assigned(self) -> None:
        incident = _make_incident()
        assert incident.incident_id is not None

    def test_two_incidents_have_different_ids(self) -> None:
        assert _make_incident().incident_id != _make_incident().incident_id

    def test_creates_incident_with_flight_reference(self) -> None:
        incident = _make_incident(flight_id=_FLIGHT_ID)
        assert incident.flight_id == _FLIGHT_ID

    def test_creates_incident_with_baggage_reference(self) -> None:
        incident = _make_incident(baggage_id=_BAGGAGE_ID)
        assert incident.baggage_id == _BAGGAGE_ID

    def test_creates_incident_with_in_progress_status(self) -> None:
        incident = _make_incident(status=IncidentStatus.IN_PROGRESS)
        assert incident.status == IncidentStatus.IN_PROGRESS

    def test_creates_incident_with_critical_priority(self) -> None:
        incident = _make_incident(priority=IncidentPriority.CRITICAL)
        assert incident.priority == IncidentPriority.CRITICAL

    def test_references_reporter_by_id(self) -> None:
        incident = _make_incident()
        assert incident.reported_by == _USER_ID

    def test_raises_when_title_is_empty(self) -> None:
        with pytest.raises(ValueError, match="Title must not be empty"):
            _make_incident(title="")

    def test_raises_when_title_is_whitespace(self) -> None:
        with pytest.raises(ValueError, match="Title must not be empty"):
            _make_incident(title="   ")

    def test_raises_when_description_is_empty(self) -> None:
        with pytest.raises(ValueError, match="Description must not be empty"):
            _make_incident(description="")

    def test_raises_when_description_is_whitespace(self) -> None:
        with pytest.raises(ValueError, match="Description must not be empty"):
            _make_incident(description="   ")
