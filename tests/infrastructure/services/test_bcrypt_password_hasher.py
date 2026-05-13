from app.infrastructure.services.bcrypt_password_hasher import (
    BcryptPasswordHasher)


class TestBcryptPasswordHasher:
    def setup_method(self) -> None:
        self.hasher = BcryptPasswordHasher()

    def test_hash_returns_string(self) -> None:
        result = self.hasher.hash("secret123")

        assert isinstance(result, str)

    def test_hash_is_not_plain_text(self) -> None:
        result = self.hasher.hash("secret123")

        assert result != "secret123"

    def test_two_hashes_of_same_password_differ(self) -> None:
        first = self.hasher.hash("secret123")
        second = self.hasher.hash("secret123")

        assert first != second

    def test_verify_returns_true_for_correct_password(self) -> None:
        hashed = self.hasher.hash("secret123")

        assert self.hasher.verify("secret123", hashed) is True

    def test_verify_returns_false_for_wrong_password(self) -> None:
        hashed = self.hasher.hash("secret123")

        assert self.hasher.verify("wrong_password", hashed) is False

    def test_verify_returns_false_for_empty_password(self) -> None:
        hashed = self.hasher.hash("secret123")

        assert self.hasher.verify("", hashed) is False

    def test_hash_empty_password(self) -> None:
        result = self.hasher.hash("")

        assert isinstance(result, str)
        assert self.hasher.verify("", result) is True
