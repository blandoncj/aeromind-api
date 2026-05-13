from app.domain.exceptions.domain_error import DomainError


class InvalidDocumentError(DomainError):
    def __init__(
        self,
        message: str = "Invalid document.",
        context: dict | None = None
    ) -> None:
        super().__init__(
            code="INVALID_DOCUMENT",
            message=message,
            context=context
        )
