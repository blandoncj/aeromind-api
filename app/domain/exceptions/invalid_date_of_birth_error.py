from app.domain.exceptions.domain_error import DomainError


class InvalidDateOfBirthError(DomainError):
    def __init__(
        self,
        message: str = "Invalid date of birth.",
        context: dict | None = None
    ) -> None:
        super().__init__(
            code="INVALID_DATE_OF_BIRTH",
            message=message,
            context=context
        )
