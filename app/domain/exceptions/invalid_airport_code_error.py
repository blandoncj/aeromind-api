from app.domain.exceptions.domain_error import DomainError


class InvalidAirportCodeError(DomainError):
    def __init__(
        self,
        message: str = "Invalid airport code.",
        context: dict | None = None,
    ) -> None:
        super().__init__(
            code="INVALID_AIRPORT_CODE",
            message=message,
            context=context,
        )
