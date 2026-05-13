from app.domain.exceptions.domain_error import DomainError


class InvalidSeatNumberError(DomainError):
    def __init__(
        self,
        message: str = "Invalid seat number.",
        context: dict | None = None,
    ) -> None:
        super().__init__(
            code="INVALID_SEAT_NUMBER",
            message=message,
            context=context,
        )
