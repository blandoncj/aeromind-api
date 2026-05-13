from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import jwt

from app.application.ports.token_service import TokenService
from app.domain.enums.role import Role
from app.infrastructure.config.settings import settings


class JwtTokenService(TokenService):
    def generate(self, user_id: UUID, role: Role) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expiration_minutes
        )
        payload = {
            "sub": str(user_id),
            "role": role.value,
            "exp": expire,
        }
        return jwt.encode(
            payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
