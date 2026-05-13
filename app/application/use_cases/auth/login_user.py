from app.application.dtos.auth_dtos import LoginUserInput, LoginUserOutput
from app.application.exceptions.invalid_credentials_error import (
    InvalidCredentialsError)
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.token_service import TokenService
from app.application.ports.user_repository import UserRepository
from app.domain.value_objects.email import Email


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def execute(self, input: LoginUserInput) -> LoginUserOutput:
        email = Email(input.email)

        user = await self._user_repository.find_by_email(email)
        if user is None or not self._password_hasher.verify(
                input.password, user.password_hash):
            raise InvalidCredentialsError()

        token = self._token_service.generate(user.user_id, user.role)

        return LoginUserOutput(
            access_token=token,
            token_type="bearer",
            user_id=user.user_id,
            email=user.email.value,
            role=user.role
        )
