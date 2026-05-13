from app.application.exceptions.application_error import ApplicationError


class BaggageNotFoundError(ApplicationError):
    def __init__(self, tag: str) -> None:
        super().__init__(
            code="BAGGAGE_NOT_FOUND",
            message="Baggage not found.",
            context={"tag": tag}
        )
