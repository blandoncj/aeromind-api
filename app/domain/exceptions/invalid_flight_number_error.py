from app.domain.exceptions.domain_error import DomainError


class InvalidFlightNumberError(DomainError):
    def __init__(
        self,
        message: str = "Invalid flight number.",
        context: dict | None = None,
    ) -> None:
        super().__init__(
            code="INVALID_FLIGHT_NUMBER",
            message=message,
            context=context,
        )
