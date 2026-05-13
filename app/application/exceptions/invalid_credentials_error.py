from app.application.exceptions.application_error import ApplicationError


class InvalidCredentialsError(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="Email or password is incorrect."
        )
