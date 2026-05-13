from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums.gender import Gender
from app.domain.enums.role import Role
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.nationality import Nationality
from app.domain.value_objects.phone_number import PhoneNumber


@dataclass
class User:
    document: Document
    nationality: Nationality
    gender: Gender
    first_name: str
    first_lastname: str
    email: Email
    password_hash: str
    role: Role
    phone_number: PhoneNumber
    second_lastname: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    user_id: UUID = field(default_factory=uuid4)
