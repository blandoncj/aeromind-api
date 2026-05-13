from uuid import UUID

from app.application.exceptions.application_error import ApplicationError


class FlightNotFoundError(ApplicationError):
    def __init__(self, flight_id: UUID) -> None:
        super().__init__(
            code="FLIGHT_NOT_FOUND",
            message="Flight not found.",
            context={"flight_id": str(flight_id)}
        )
