from app.domain.exceptions.domain_error import DomainError


class InvalidBaggageTagError(DomainError):
    def __init__(
        self,
        message: str = "Invalid baggage tag.",
        context: dict | None = None,
    ) -> None:
        super().__init__(
            code="INVALID_BAGGAGE_TAG",
            message=message,
            context=context,
        )
