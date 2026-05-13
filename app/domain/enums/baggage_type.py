from enum import StrEnum


class BaggageType(StrEnum):
    CHECKED = "CHECKED"
    CARRY_ON = "CARRY_ON"
    OVERSIZED = "OVERSIZED"
    SPECIAL = "SPECIAL"

    @property
    def label(self) -> str:
        return {
            BaggageType.CHECKED: "Equipaje de bodega",
            BaggageType.CARRY_ON: "Equipaje de mano",
            BaggageType.OVERSIZED: "Sobredimensionado",
            BaggageType.SPECIAL: "Especial",
        }[self]
