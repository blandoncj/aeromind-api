from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.enums.document_type import DocumentType
from app.domain.enums.gender import Gender
from app.domain.enums.role import Role
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.nationality import Nationality
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.database.models.user_model import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_email(self, email: Email) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.value)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_id(self, user_id: UUID) -> User | None:
        model = await self._session.get(UserModel, user_id)
        return self._to_entity(model) if model else None

    async def save(self, user: User) -> None:
        model = await self._session.get(UserModel, user.user_id)
        if model is None:
            self._session.add(self._to_model(user))
        else:
            self._update_model(model, user)
        await self._session.flush()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            user_id=model.user_id,
            document=Document(
                type=DocumentType(model.document_type),
                number=model.document_number,
            ),
            nationality=Nationality(code=model.nationality),
            gender=Gender(model.gender),
            first_name=model.first_name,
            first_lastname=model.first_lastname,
            second_lastname=model.second_lastname,
            email=Email(value=model.email),
            password_hash=model.password_hash,
            role=Role(model.role),
            phone_number=PhoneNumber(value=model.phone_number),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, user: User) -> UserModel:
        return UserModel(
            user_id=user.user_id,
            document_type=user.document.type.value,
            document_number=user.document.number,
            nationality=user.nationality.code,
            gender=user.gender.value,
            first_name=user.first_name,
            first_lastname=user.first_lastname,
            second_lastname=user.second_lastname,
            email=user.email.value,
            password_hash=user.password_hash,
            role=user.role.value,
            phone_number=user.phone_number.value,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def _update_model(self, model: UserModel, user: User) -> None:
        model.document_type = user.document.type.value
        model.document_number = user.document.number
        model.nationality = user.nationality.code
        model.gender = user.gender.value
        model.first_name = user.first_name
        model.first_lastname = user.first_lastname
        model.second_lastname = user.second_lastname
        model.email = user.email.value
        model.password_hash = user.password_hash
        model.role = user.role.value
        model.phone_number = user.phone_number.value
        model.is_active = user.is_active
        model.updated_at = user.updated_at
