from datetime import datetime, timezone
from unittest.mock import patch
from uuid import uuid4

import pytest
from jose import jwt

from app.domain.enums.role import Role
from app.infrastructure.config.settings import settings
from app.infrastructure.services.jwt_token_service import JwtTokenService


class TestJwtTokenService:
    def setup_method(self) -> None:
        self.service = JwtTokenService()

    def test_generate_returns_string(self) -> None:
        token = self.service.generate(uuid4(), Role.PASSENGER)

        assert isinstance(token, str)

    def test_token_contains_user_id(self) -> None:
        user_id = uuid4()

        token = self.service.generate(user_id, Role.PASSENGER)

        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        assert payload["sub"] == str(user_id)

    def test_token_contains_role(self) -> None:
        token = self.service.generate(uuid4(), Role.ADMIN)

        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        assert payload["role"] == Role.ADMIN.value

    def test_token_contains_expiration(self) -> None:
        token = self.service.generate(uuid4(), Role.PASSENGER)

        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        assert "exp" in payload

    def test_token_expires_after_configured_minutes(self) -> None:
        now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        with patch(
                "app.infrastructure.services.jwt_token_service.datetime"
        ) as mock_dt:
            mock_dt.now.return_value = now

            token = self.service.generate(uuid4(), Role.PASSENGER)

        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[
                settings.jwt_algorithm],
            options={"verify_exp": False},
        )
        expected_exp = int(now.timestamp()) + \
            settings.jwt_expiration_minutes * 60
        assert payload["exp"] == pytest.approx(expected_exp, abs=1)

    def test_different_users_get_different_tokens(self) -> None:
        token_a = self.service.generate(uuid4(), Role.PASSENGER)
        token_b = self.service.generate(uuid4(), Role.PASSENGER)

        assert token_a != token_b
