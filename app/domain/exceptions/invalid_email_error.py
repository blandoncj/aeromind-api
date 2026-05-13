from app.domain.exceptions.domain_error import DomainError


class InvalidEmailError(DomainError):
    def __init__(
        self,
        message: str = "Invalid email.",
        context: dict | None = None
    ) -> None:
        super().__init__(
            code="INVALID_EMAIL",
            message=message,
            context=context
        )
