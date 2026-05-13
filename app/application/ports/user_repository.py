from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User
from app.domain.value_objects.email import Email


class UserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: Email) -> User | None: ...

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> None: ...
