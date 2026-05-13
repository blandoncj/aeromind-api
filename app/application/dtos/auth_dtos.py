from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.document_type import DocumentType
from app.domain.enums.gender import Gender
from app.domain.enums.role import Role


@dataclass(frozen=True)
class RegisterUserInput:
    email: str
    password: str
    first_name: str
    first_lastname: str
    document_type: DocumentType
    document_number: str
    nationality_code: str
    gender: Gender
    phone_number: str
    second_lastname: str | None = None
    role: Role = Role.PASSENGER


@dataclass(frozen=True)
class RegisterUserOutput:
    user_id: UUID
    email: str
    first_name: str
    first_lastname: str
    role: Role


@dataclass(frozen=True)
class LoginUserInput:
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserOutput:
    access_token: str
    token_type: str
    user_id: UUID
    email: str
    role: Role
