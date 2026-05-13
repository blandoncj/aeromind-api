from enum import StrEnum


class BaggageStatus(StrEnum):
    CHECKED_IN = "CHECKED_IN"
    LOADED = "LOADED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    MISSING = "MISSING"
    DAMAGED = "DAMAGED"

    @property
    def label(self) -> str:
        return {
            BaggageStatus.CHECKED_IN: "Registrado",
            BaggageStatus.LOADED: "Cargado",
            BaggageStatus.IN_TRANSIT: "En tránsito",
            BaggageStatus.DELIVERED: "Entregado",
            BaggageStatus.MISSING: "Extraviado",
            BaggageStatus.DAMAGED: "Dañado",
        }[self]
