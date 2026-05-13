from enum import StrEnum


class Gender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"

    @property
    def label(self) -> str:
        return {
            Gender.MALE: "Masculino",
            Gender.FEMALE: "Femenino",
            Gender.OTHER: "Otro",
            Gender.PREFER_NOT_TO_SAY: "Prefiero no decirlo"
        }[self]
