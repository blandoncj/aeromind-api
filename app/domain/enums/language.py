from enum import StrEnum


class Language(StrEnum):
    SPANISH = "SPANISH"
    ENGLISH = "ENGLISH"
    FRENCH = "FRENCH"
    PORTUGUESE = "PORTUGUESE"

    @property
    def short_label(self) -> str:
        return {
            Language.SPANISH: "ES",
            Language.ENGLISH: "EN",
            Language.FRENCH: "FR",
            Language.PORTUGUESE: "PT"
        }[self]

    @property
    def label(self) -> str:
        return {
            Language.SPANISH: "Español",
            Language.ENGLISH: "English",
            Language.FRENCH: "Français",
            Language.PORTUGUESE: "Português"
        }[self]
