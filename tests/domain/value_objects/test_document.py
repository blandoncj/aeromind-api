import pytest

from app.domain.enums.document_type import DocumentType
from app.domain.exceptions.invalid_document_error import InvalidDocumentError
from app.domain.value_objects.document import Document


class TestDocumentCitizenId:
    def test_valid_citizen_id(self) -> None:
        doc = Document(DocumentType.CITIZEN_ID, "123456")
        assert doc.number == "123456"

    def test_valid_citizen_id_max_length(self) -> None:
        doc = Document(DocumentType.CITIZEN_ID, "1234567890")
        assert doc.number == "1234567890"

    def test_raises_when_citizen_id_too_short(self) -> None:
        with pytest.raises(InvalidDocumentError) as exc_info:
            Document(DocumentType.CITIZEN_ID, "12345")
        assert exc_info.value.code == "INVALID_DOCUMENT"

    def test_raises_when_citizen_id_too_long(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.CITIZEN_ID, "12345678901")

    def test_raises_when_citizen_id_has_letters(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.CITIZEN_ID, "12345A")


class TestDocumentIdentityCard:
    def test_valid_identity_card(self) -> None:
        doc = Document(DocumentType.IDENTITY_CARD, "1234567890")
        assert doc.number == "1234567890"

    def test_raises_when_identity_card_too_short(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.IDENTITY_CARD, "123456789")

    def test_raises_when_identity_card_too_long(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.IDENTITY_CARD, "1234567890123")


class TestDocumentForeignerId:
    def test_valid_foreigner_id(self) -> None:
        doc = Document(DocumentType.FOREIGNER_ID, "ABC123")
        assert doc.number == "ABC123"

    def test_raises_when_foreigner_id_too_long(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.FOREIGNER_ID, "A" * 16)

    def test_raises_when_foreigner_id_has_special_chars(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.FOREIGNER_ID, "ABC-123")


class TestDocumentPassport:
    def test_valid_passport(self) -> None:
        doc = Document(DocumentType.PASSPORT, "AB1234567")
        assert doc.number == "AB1234567"

    def test_raises_when_passport_too_short(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.PASSPORT, "ABCD")

    def test_raises_when_passport_too_long(self) -> None:
        with pytest.raises(InvalidDocumentError):
            Document(DocumentType.PASSPORT, "A" * 21)
