from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.domain.enums.role import Role
from app.infrastructure.config.settings import settings

_bearer_scheme = HTTPBearer()


@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID
    role: Role


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(_bearer_scheme)
    ],
) -> CurrentUser:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return CurrentUser(
            user_id=UUID(payload["sub"]),
            role=Role(payload["role"]),
        )
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


def require_roles(*roles: Role):  # type: ignore[no-untyped-def]
    def guard(current_user: CurrentUserDep) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return current_user

    return guard
