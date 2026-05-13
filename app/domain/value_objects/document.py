import re
from dataclasses import dataclass
from typing import Callable

from app.domain.enums.document_type import DocumentType
from app.domain.exceptions.invalid_document_error import InvalidDocumentError


@dataclass(frozen=True)
class Document:
    type: DocumentType
    number: str

    def __post_init__(self) -> None:
        normalized = self.number.strip().upper()
        object.__setattr__(self, 'number', normalized)
        self._validate_by_type(normalized)

    def _validate_by_type(self, value: str) -> None:
        validators: dict[DocumentType, Callable[[str], None]] = {
            DocumentType.CITIZEN_ID: self._validate_citizen_id,
            DocumentType.IDENTITY_CARD: self._validate_identity_card,
            DocumentType.FOREIGNER_ID: self._validate_foreigner_id,
            DocumentType.PASSPORT: self._validate_passport
        }
        validators[self.type](value)

    def _validate_citizen_id(self, value: str) -> None:
        self._validate_numeric(value)
        if not (6 <= len(value) <= 10):
            raise InvalidDocumentError(
                message="Citizen ID must be between 6 and 10 digits long.",
                context={
                    "document_type": self.type.value,
                    "number": value,
                    "min_length": 6,
                    "max_length": 10
                }
            )

    def _validate_identity_card(self, value: str) -> None:
        self._validate_numeric(value)
        if not (10 <= len(value) <= 12):
            raise InvalidDocumentError(
                message="Identity Card must be between 10 and 12 digits long.",
                context={
                    "document_type": self.type.value,
                    "number": value,
                    "min_length": 10,
                    "max_length": 12
                }
            )

    def _validate_foreigner_id(self, value: str) -> None:
        self._validate_alphanumeric(value)
        if len(value) > 15:
            raise InvalidDocumentError(
                message="Foreigner ID must be at most 15 characters long.",
                context={
                    "document_type": self.type.value,
                    "number": value,
                    "max_length": 15
                }
            )

    def _validate_passport(self, value: str) -> None:
        self._validate_alphanumeric(value)
        if not (5 <= len(value) <= 20):
            raise InvalidDocumentError(
                message="Passport must be between 5 and 20 characters long.",
                context={
                    "document_type": self.type.value,
                    "number": value,
                    "min_length": 5,
                    "max_length": 20
                }
            )

    @staticmethod
    def _validate_numeric(value: str) -> None:
        if not re.fullmatch(r"\d+", value):
            raise InvalidDocumentError(
                message="Document number must contain digits only.",
                context={"number": value}
            )

    @staticmethod
    def _validate_alphanumeric(value: str) -> None:
        if not re.fullmatch(r"[A-Z0-9]+", value):
            raise InvalidDocumentError(
                message="""
                    Document number must contain alphanumeric characters only.
                """,
                context={"number": value}
            )
