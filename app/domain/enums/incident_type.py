from enum import StrEnum


class IncidentType(StrEnum):
    LOST_BAGGAGE = "LOST_BAGGAGE"
    DAMAGED_BAGGAGE = "DAMAGED_BAGGAGE"
    FLIGHT_DELAY = "FLIGHT_DELAY"
    FLIGHT_CANCELLATION = "FLIGHT_CANCELLATION"
    SECURITY = "SECURITY"
    MEDICAL = "MEDICAL"
    OTHER = "OTHER"

    @property
    def label(self) -> str:
        return {
            IncidentType.LOST_BAGGAGE: "Equipaje extraviado",
            IncidentType.DAMAGED_BAGGAGE: "Equipaje dañado",
            IncidentType.FLIGHT_DELAY: "Retraso de vuelo",
            IncidentType.FLIGHT_CANCELLATION: "Cancelación de vuelo",
            IncidentType.SECURITY: "Seguridad",
            IncidentType.MEDICAL: "Médico",
            IncidentType.OTHER: "Otro",
        }[self]
