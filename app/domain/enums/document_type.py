from enum import StrEnum


class DocumentType(StrEnum):
    CITIZEN_ID = "CITIZEN_ID"
    IDENTITY_CARD = "IDENTITY_CARD"
    FOREIGNER_ID = "FOREIGNER_ID"
    PASSPORT = "PASSPORT"

    @property
    def short_label(self) -> str:
        return {
            DocumentType.CITIZEN_ID: "CC",
            DocumentType.IDENTITY_CARD: "TI",
            DocumentType.FOREIGNER_ID: "CE",
            DocumentType.PASSPORT: "PAS"
        }[self]

    @property
    def label(self) -> str:
        return {
            DocumentType.CITIZEN_ID: "Cédula de ciudadanía",
            DocumentType.IDENTITY_CARD: "Tarjeta de identidad",
            DocumentType.FOREIGNER_ID: "Cédula de extranjería",
            DocumentType.PASSPORT: "Pasaporte"
        }[self]
