import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dtos.auth_dtos import LoginUserInput, LoginUserOutput
from app.application.exceptions.invalid_credentials_error import InvalidCredentialsError
from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.domain.enums.role import Role


def _make_user(role: Role = Role.PASSENGER, is_active: bool = True) -> MagicMock:
    user = MagicMock()
    user.user_id = uuid4()
    user.email.value = "juan.perez@example.com"
    user.password_hash = "hashed_password"
    user.role = role
    user.is_active = is_active
    return user


def _make_use_case(
    user: object = None,
    password_valid: bool = True,
    token: str = "jwt.token.here",
) -> tuple[LoginUserUseCase, AsyncMock, MagicMock, MagicMock]:
    repo = AsyncMock()
    repo.find_by_email.return_value = user

    hasher = MagicMock()
    hasher.verify.return_value = password_valid

    token_service = MagicMock()
    token_service.generate.return_value = token

    return LoginUserUseCase(repo, hasher, token_service), repo, hasher, token_service


class TestLoginUserUseCase:
    def test_returns_output_on_valid_credentials(self) -> None:
        user = _make_user()
        use_case, _, _, _ = _make_use_case(user=user)
        input = LoginUserInput(email="juan.perez@example.com", password="PlainPass")

        result = asyncio.run(use_case.execute(input))

        assert isinstance(result, LoginUserOutput)
        assert result.access_token == "jwt.token.here"
        assert result.token_type == "bearer"
        assert result.email == "juan.perez@example.com"
        assert result.user_id == user.user_id
        assert result.role == Role.PASSENGER

    def test_raises_when_user_not_found(self) -> None:
        use_case, _, _, _ = _make_use_case(user=None)
        input = LoginUserInput(email="noexiste@example.com", password="any")

        with pytest.raises(InvalidCredentialsError) as exc_info:
            asyncio.run(use_case.execute(input))

        assert exc_info.value.code == "INVALID_CREDENTIALS"

    def test_raises_when_password_is_wrong(self) -> None:
        use_case, _, _, _ = _make_use_case(user=_make_user(), password_valid=False)
        input = LoginUserInput(email="juan.perez@example.com", password="WrongPass")

        with pytest.raises(InvalidCredentialsError):
            asyncio.run(use_case.execute(input))

    def test_does_not_generate_token_on_failed_auth(self) -> None:
        use_case, _, _, token_service = _make_use_case(user=None)

        with pytest.raises(InvalidCredentialsError):
            asyncio.run(use_case.execute(LoginUserInput(email="x@x.com", password="y")))

        token_service.generate.assert_not_called()

    def test_generates_token_with_correct_user_data(self) -> None:
        user = _make_user(role=Role.OPERATOR)
        use_case, _, _, token_service = _make_use_case(user=user)

        asyncio.run(use_case.execute(LoginUserInput(email="juan.perez@example.com", password="pass")))

        token_service.generate.assert_called_once_with(user.user_id, Role.OPERATOR)

    def test_verifies_password_against_stored_hash(self) -> None:
        user = _make_user()
        use_case, _, hasher, _ = _make_use_case(user=user)

        asyncio.run(use_case.execute(LoginUserInput(email="juan.perez@example.com", password="PlainPass")))

        hasher.verify.assert_called_once_with("PlainPass", "hashed_password")
