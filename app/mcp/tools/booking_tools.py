from uuid import UUID

from mcp.server.fastmcp import FastMCP

from app.application.dtos.booking_dtos import (
    GetBookingInput, GetUserBookingsInput)
from app.application.use_cases.bookings.get_booking import GetBookingUseCase
from app.application.use_cases.bookings.get_user_bookings import (
    GetUserBookingsUseCase)
from app.infrastructure.database.session import AsyncSessionFactory
from app.infrastructure.repositories.sqlalchemy_booking_repository import (
    SqlAlchemyBookingRepository,
)
from app.mcp.tools._utils import serialize


def register_booking_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def get_booking(booking_reference: str) -> str:
        """Get booking details by reference code.

        Args:
            booking_reference: Booking reference code (e.g. ABC123)
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyBookingRepository(session)
                result = await GetBookingUseCase(repo).execute(
                    GetBookingInput(booking_reference=booking_reference)
                )
        return serialize(result)

    @mcp.tool()
    async def get_user_bookings(user_id: str) -> str:
        """Get all bookings for a specific user.

        Args:
            user_id: UUID of the user
        """
        async with AsyncSessionFactory() as session:
            async with session.begin():
                repo = SqlAlchemyBookingRepository(session)
                results = await GetUserBookingsUseCase(repo).execute(
                    GetUserBookingsInput(user_id=UUID(user_id))
                )
        return serialize(results)
