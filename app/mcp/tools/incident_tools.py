from uuid import UUID

from mcp.server.fastmcp import FastMCP

from app.application.dtos.incident_dtos import (
    CreateIncidentInput, GetIncidentsInput)
from app.application.use_cases.incidents.create_incident import (
    CreateIncidentUseCase)
from app.application.use_cases.incidents.get_incidents import (
    GetIncidentsUseCase)
from app.domain.enums.incident_priority import IncidentPriority
from app.domain.enums.incident_status import IncidentStatus
from app.domain.enums.incident_type import IncidentType
from app.infrastructure.database.session import AsyncSessionFactory
from app.infrastructure.repositories.sqlalchemy_incident_repository import (
    SqlAlchemyIncidentRepository,
)
from app.mcp.tools._utils import serialize


def register_incident_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def create_incident(
        reported_by: str,
        title: str,
        description: str,
        incident_type: str,
        priority: str,
        flight_id: str = "",
        baggage_id: str = "",
    ) -> str:
        """Create a new operational incident.

        Args:
            reported_by: UUID of the user reporting the incident
            title: Short title describing the incident
            description: Detailed description of the incident
            incident_type: LOST_BAGGAGE | DAMAGED_BAGGAGE | FLIGHT_DELAY | FLIGHT_CANCELLATION | SECURITY | MEDICAL | OTHER
            priority: LOW | MEDIUM | HIGH | CRITICAL
            flight_id: Optional UUID of the related flight
            baggage_id: Optional UUID of the related baggage
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyIncidentRepository(session)
                result = await CreateIncidentUseCase(repo).execute(
                    CreateIncidentInput(
                        reported_by=UUID(reported_by),
                        title=title,
                        description=description,
                        incident_type=IncidentType(incident_type),
                        priority=IncidentPriority(priority),
                        flight_id=UUID(flight_id) if flight_id else None,
                        baggage_id=UUID(baggage_id) if baggage_id else None,
                    )
                )
        return serialize(result)

    @mcp.tool()
    async def get_incidents(
        status: str = "",
        incident_type: str = "",
        priority: str = "",
        reported_by: str = "",
    ) -> str:
        """List operational incidents with optional filters.

        Args:
            status: OPEN | IN_PROGRESS | RESOLVED | CLOSED (optional)
            incident_type: LOST_BAGGAGE | DAMAGED_BAGGAGE | FLIGHT_DELAY | FLIGHT_CANCELLATION | SECURITY | MEDICAL | OTHER (optional)
            priority: LOW | MEDIUM | HIGH | CRITICAL (optional)
            reported_by: UUID of reporter (optional)
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyIncidentRepository(session)
                results = await GetIncidentsUseCase(repo).execute(
                    GetIncidentsInput(
                        status=IncidentStatus(status) if status else None,
                        incident_type=IncidentType(
                            incident_type) if incident_type else None,
                        priority=IncidentPriority(
                            priority) if priority else None,
                        reported_by=UUID(reported_by) if reported_by else None,
                    )
                )
        return serialize(results)
