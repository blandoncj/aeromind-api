from app.domain.exceptions.domain_error import DomainError


class InvalidPhoneNumberError(DomainError):
    def __init__(
        self,
        message: str = "Invalid phone number.",
        context: dict | None = None
    ) -> None:
        super().__init__(
            code="INVALID_PHONE_NUMBER",
            message=message,
            context=context
        )
