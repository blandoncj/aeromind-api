from app.infrastructure.services.bcrypt_password_hasher import (
    BcryptPasswordHasher)

_TEST_PASSWORD = "secret123"  # NOSONAR
_WRONG_PASSWORD = "wrong_password"  # NOSONAR


class TestBcryptPasswordHasher:
    def setup_method(self) -> None:
        self.hasher = BcryptPasswordHasher()

    def test_hash_returns_string(self) -> None:
        result = self.hasher.hash(_TEST_PASSWORD)

        assert isinstance(result, str)

    def test_hash_is_not_plain_text(self) -> None:
        result = self.hasher.hash(_TEST_PASSWORD)

        assert result != _TEST_PASSWORD

    def test_two_hashes_of_same_password_differ(self) -> None:
        first = self.hasher.hash(_TEST_PASSWORD)
        second = self.hasher.hash(_TEST_PASSWORD)

        assert first != second

    def test_verify_returns_true_for_correct_password(self) -> None:
        hashed = self.hasher.hash(_TEST_PASSWORD)

        assert self.hasher.verify(_TEST_PASSWORD, hashed) is True

    def test_verify_returns_false_for_wrong_password(self) -> None:
        hashed = self.hasher.hash(_TEST_PASSWORD)

        assert self.hasher.verify(_WRONG_PASSWORD, hashed) is False

    def test_verify_returns_false_for_empty_password(self) -> None:
        hashed = self.hasher.hash(_TEST_PASSWORD)

        assert self.hasher.verify("", hashed) is False

    def test_hash_empty_password(self) -> None:
        result = self.hasher.hash("")

        assert isinstance(result, str)
        assert self.hasher.verify("", result) is True
