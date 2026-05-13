from app.domain.entities.user import User
from app.domain.enums.document_type import DocumentType
from app.domain.enums.gender import Gender
from app.domain.enums.role import Role
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.nationality import Nationality
from app.domain.value_objects.phone_number import PhoneNumber


_TEST_HASH = "hashed_password"  # NOSONAR


def _make_user(**overrides) -> User:  # type: ignore[no-untyped-def]
    defaults = {
        "document": Document(DocumentType.CITIZEN_ID, "1234567890"),
        "nationality": Nationality("CO"),
        "gender": Gender.MALE,
        "first_name": "Juan",
        "first_lastname": "Pérez",
        "email": Email("juan.perez@example.com"),
        "password_hash": _TEST_HASH,
        "role": Role.PASSENGER,
        "phone_number": PhoneNumber("+573001234567"),
    }
    defaults.update(overrides)
    return User(**defaults)


class TestUser:
    def test_creates_user_with_defaults(self) -> None:
        user = _make_user()
        assert user.is_active is True
        assert user.second_lastname is None

    def test_user_id_is_assigned(self) -> None:
        user = _make_user()
        assert user.user_id is not None

    def test_two_users_have_different_ids(self) -> None:
        assert _make_user().user_id != _make_user().user_id

    def test_creates_user_with_second_lastname(self) -> None:
        user = _make_user(second_lastname="García")
        assert user.second_lastname == "García"

    def test_creates_admin_user(self) -> None:
        user = _make_user(role=Role.ADMIN)
        assert user.role == Role.ADMIN

    def test_creates_operator_user(self) -> None:
        user = _make_user(role=Role.OPERATOR)
        assert user.role == Role.OPERATOR

    def test_user_can_be_deactivated(self) -> None:
        user = _make_user(is_active=False)
        assert user.is_active is False
