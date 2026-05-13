from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.enums.role import Role


class TokenService(ABC):
    @abstractmethod
    def generate(self, user_id: UUID, role: Role) -> str: ...
