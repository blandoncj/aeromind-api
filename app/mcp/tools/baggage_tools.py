from uuid import UUID

from mcp.server.fastmcp import FastMCP

from app.application.dtos.baggage_dtos import (
    ReportLostBaggageInput, TrackBaggageInput)
from app.application.use_cases.baggage.report_lost_baggage import (
    ReportLostBaggageUseCase)
from app.application.use_cases.baggage.track_baggage import TrackBaggageUseCase
from app.infrastructure.database.session import AsyncSessionFactory
from app.infrastructure.repositories.sqlalchemy_baggage_repository import (
    SqlAlchemyBaggageRepository,
)
from app.infrastructure.repositories.sqlalchemy_incident_repository import (
    SqlAlchemyIncidentRepository,
)
from app.mcp.tools._utils import serialize


def register_baggage_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def track_baggage(tag: str) -> str:
        """Track the current status of baggage by its tag number.

        Args:
            tag: Baggage tag number (e.g. 0014123456)
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyBaggageRepository(session)
                result = await TrackBaggageUseCase(repo).execute(
                    TrackBaggageInput(tag=tag)
                )
        return serialize(result)

    @mcp.tool()
    async def report_lost_baggage(
            tag: str, reported_by: str, description: str = "") -> str:
        """Report baggage as lost and automatically create an incident.

        Args:
            tag: Baggage tag number
            reported_by: UUID of the user reporting the loss
            description: Optional description of the situation
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                baggage_repo = SqlAlchemyBaggageRepository(session)
                incident_repo = SqlAlchemyIncidentRepository(session)
                result = await ReportLostBaggageUseCase(
                    baggage_repo, incident_repo).execute(
                    ReportLostBaggageInput(
                        tag=tag,
                        reported_by=UUID(reported_by),
                        description=description or None,
                    )
                )
        return serialize(result)
