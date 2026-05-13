from app.application.exceptions.application_error import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, email: str) -> None:
        super().__init__(
            code="USER_ALREADY_EXISTS",
            message="A user with this email already exists.",
            context={"email": email}
        )
