from datetime import date
from uuid import UUID

from mcp.server.fastmcp import FastMCP

from app.application.dtos.flight_dtos import GetFlightInput, SearchFlightsInput
from app.application.use_cases.flights.get_flight import GetFlightUseCase
from app.application.use_cases.flights.search_flights import (
    SearchFlightsUseCase)
from app.infrastructure.database.session import AsyncSessionFactory
from app.infrastructure.repositories.sqlalchemy_flight_repository import (
    SqlAlchemyFlightRepository,
)
from app.mcp.tools._utils import serialize


def register_flight_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def search_flights(
            origin: str, destination: str, departure_date: str) -> str:
        """Search available flights between two airports.

        Args:
            origin: IATA airport code for origin (e.g. BOG, MIA, JFK)
            destination: IATA airport code for destination (e.g. BOG, MIA, JFK)
            departure_date: Departure date in ISO format YYYY-MM-DD
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyFlightRepository(session)
                results = await SearchFlightsUseCase(repo).execute(
                    SearchFlightsInput(
                        origin=origin,
                        destination=destination,
                        departure_date=date.fromisoformat(departure_date),
                    )
                )
        return serialize(results)

    @mcp.tool()
    async def get_flight(flight_id: str) -> str:
        """Get details of a specific flight.

        Args:
            flight_id: UUID of the flight
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyFlightRepository(session)
                result = await GetFlightUseCase(repo).execute(
                    GetFlightInput(flight_id=UUID(flight_id))
                )
        return serialize(result)
