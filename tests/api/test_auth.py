from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.api.auth import CurrentUser, get_current_user, require_roles
from app.domain.enums.role import Role
from app.infrastructure.config.settings import settings

_SECRET = settings.jwt_secret_key
_ALGORITHM = settings.jwt_algorithm


def _make_token(
    user_id=None,
    role: Role = Role.PASSENGER,
    expires_delta: timedelta = timedelta(minutes=60),
) -> str:
    user_id = user_id or uuid4()
    exp = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(
        {"sub": str(user_id), "role": role.value, "exp": exp},
        _SECRET,
        algorithm=_ALGORITHM,
    )


def _credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


class TestGetCurrentUser:
    def test_returns_current_user_from_valid_token(self) -> None:
        user_id = uuid4()
        token = _make_token(user_id=user_id, role=Role.PASSENGER)

        result = get_current_user(_credentials(token))

        assert result.user_id == user_id
        assert result.role == Role.PASSENGER

    def test_returns_correct_role(self) -> None:
        token = _make_token(role=Role.ADMIN)

        result = get_current_user(_credentials(token))

        assert result.role == Role.ADMIN

    def test_raises_401_for_expired_token(self) -> None:
        token = _make_token(expires_delta=timedelta(seconds=-1))

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(_credentials(token))

        assert exc_info.value.status_code == 401

    def test_raises_401_for_invalid_signature(self) -> None:
        token = jwt.encode(
            {"sub": str(uuid4()), "role": Role.PASSENGER.value},
            "wrong-secret",
            algorithm=_ALGORITHM,
        )

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(_credentials(token))

        assert exc_info.value.status_code == 401

    def test_raises_401_for_missing_sub_claim(self) -> None:
        token = jwt.encode(
            {"role": Role.PASSENGER.value},
            _SECRET,
            algorithm=_ALGORITHM,
        )

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(_credentials(token))

        assert exc_info.value.status_code == 401

    def test_raises_401_for_invalid_role_value(self) -> None:
        token = jwt.encode(
            {"sub": str(uuid4()), "role": "INVALID_ROLE"},
            _SECRET,
            algorithm=_ALGORITHM,
        )

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(_credentials(token))

        assert exc_info.value.status_code == 401

    def test_raises_401_for_malformed_token(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(_credentials("not.a.token"))

        assert exc_info.value.status_code == 401


class TestRequireRoles:
    def _make_user(self, role: Role) -> CurrentUser:
        return CurrentUser(user_id=uuid4(), role=role)

    def test_allows_user_with_matching_role(self) -> None:
        guard = require_roles(Role.ADMIN)
        user = self._make_user(Role.ADMIN)

        result = guard(user)

        assert result == user

    def test_allows_user_with_one_of_multiple_roles(self) -> None:
        guard = require_roles(Role.OPERATOR, Role.ADMIN)
        user = self._make_user(Role.OPERATOR)

        result = guard(user)

        assert result == user

    def test_raises_403_for_insufficient_role(self) -> None:
        guard = require_roles(Role.ADMIN)
        user = self._make_user(Role.PASSENGER)

        with pytest.raises(HTTPException) as exc_info:
            guard(user)

        assert exc_info.value.status_code == 403

    def test_raises_403_when_no_roles_match(self) -> None:
        guard = require_roles(Role.ADMIN, Role.OPERATOR)
        user = self._make_user(Role.PASSENGER)

        with pytest.raises(HTTPException) as exc_info:
            guard(user)

        assert exc_info.value.status_code == 403
