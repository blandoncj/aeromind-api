from enum import StrEnum


class CabinClass(StrEnum):
    ECONOMY = "ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"

    @property
    def label(self) -> str:
        return {
            CabinClass.ECONOMY: "Económica",
            CabinClass.BUSINESS: "Ejecutiva",
            CabinClass.FIRST: "Primera clase",
        }[self]
