import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.dtos.auth_dtos import RegisterUserInput, RegisterUserOutput
from app.application.exceptions.user_already_exists_error import UserAlreadyExistsError
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.domain.enums.document_type import DocumentType
from app.domain.enums.gender import Gender
from app.domain.enums.role import Role


_TEST_PASSWORD = "SecurePass123!"  # NOSONAR
_TEST_HASH = "hashed_password"  # NOSONAR


def _make_input(**overrides: object) -> RegisterUserInput:
    defaults: dict[str, object] = {
        "email": "juan.perez@example.com",
        "password": _TEST_PASSWORD,
        "first_name": "Juan",
        "first_lastname": "Pérez",
        "document_type": DocumentType.CITIZEN_ID,
        "document_number": "1234567890",
        "nationality_code": "CO",
        "gender": Gender.MALE,
        "phone_number": "+573001234567",
    }
    defaults.update(overrides)
    return RegisterUserInput(**defaults)  # type: ignore[arg-type]


def _make_use_case(
    find_result: object = None,
    hash_return: str = _TEST_HASH,
) -> tuple[RegisterUserUseCase, AsyncMock, MagicMock]:
    repo = AsyncMock()
    repo.find_by_email.return_value = find_result
    repo.save.return_value = None

    hasher = MagicMock()
    hasher.hash.return_value = hash_return

    return RegisterUserUseCase(repo, hasher), repo, hasher


class TestRegisterUserUseCase:
    def test_returns_output_with_correct_data(self) -> None:
        use_case, _, _ = _make_use_case()
        register_input = _make_input()

        result = asyncio.run(use_case.execute(register_input))

        assert isinstance(result, RegisterUserOutput)
        assert result.email == "juan.perez@example.com"
        assert result.first_name == "Juan"
        assert result.first_lastname == "Pérez"
        assert result.role == Role.PASSENGER
        assert result.user_id is not None

    def test_hashes_password_before_saving(self) -> None:
        use_case, _, hasher = _make_use_case()

        asyncio.run(use_case.execute(_make_input(password="PlainPass")))  # NOSONAR

        hasher.hash.assert_called_once_with("PlainPass")  # NOSONAR

    def test_saves_user_to_repository(self) -> None:
        use_case, repo, _ = _make_use_case()

        asyncio.run(use_case.execute(_make_input()))

        repo.save.assert_called_once()

    def test_raises_when_email_already_exists(self) -> None:
        existing_user = MagicMock()
        use_case, _, _ = _make_use_case(find_result=existing_user)

        with pytest.raises(UserAlreadyExistsError) as exc_info:
            asyncio.run(use_case.execute(_make_input()))

        assert exc_info.value.code == "USER_ALREADY_EXISTS"

    def test_does_not_save_when_email_already_exists(self) -> None:
        existing_user = MagicMock()
        use_case, repo, _ = _make_use_case(find_result=existing_user)

        with pytest.raises(UserAlreadyExistsError):
            asyncio.run(use_case.execute(_make_input()))

        repo.save.assert_not_called()

    def test_assigns_passenger_role_by_default(self) -> None:
        use_case, _, _ = _make_use_case()

        result = asyncio.run(use_case.execute(_make_input()))

        assert result.role == Role.PASSENGER

    def test_accepts_explicit_admin_role(self) -> None:
        use_case, _, _ = _make_use_case()

        result = asyncio.run(use_case.execute(_make_input(role=Role.ADMIN)))

        assert result.role == Role.ADMIN

    def test_normalizes_email_to_lowercase(self) -> None:
        use_case, _, _ = _make_use_case()

        result = asyncio.run(use_case.execute(_make_input(email="JUAN.PEREZ@EXAMPLE.COM")))

        assert result.email == "juan.perez@example.com"