from app.application.dtos.auth_dtos import (
    RegisterUserInput, RegisterUserOutput)
from app.application.exceptions.user_already_exists_error import (
    UserAlreadyExistsError)
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.nationality import Nationality
from app.domain.value_objects.phone_number import PhoneNumber


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, input: RegisterUserInput) -> RegisterUserOutput:
        email = Email(input.email)

        existing = await self._user_repository.find_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError(email.value)

        user = User(
            email=email,
            password_hash=self._password_hasher.hash(input.password),
            first_name=input.first_name,
            first_lastname=input.first_lastname,
            second_lastname=input.second_lastname,
            document=Document(type=input.document_type,
                              number=input.document_number),
            nationality=Nationality(code=input.nationality_code),
            gender=input.gender,
            phone_number=PhoneNumber(input.phone_number),
            role=input.role
        )

        await self._user_repository.save(user)

        return RegisterUserOutput(
            user_id=user.user_id,
            email=user.email.value,
            first_name=user.first_name,
            first_lastname=user.first_lastname,
            role=user.role
        )
