from app.domain.exceptions.domain_error import DomainError


class InvalidBookingReferenceError(DomainError):
    def __init__(
        self,
        message: str = "Invalid booking reference.",
        context: dict | None = None,
    ) -> None:
        super().__init__(
            code="INVALID_BOOKING_REFERENCE",
            message=message,
            context=context,
        )
