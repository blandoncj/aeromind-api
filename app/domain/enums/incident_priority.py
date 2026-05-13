from enum import StrEnum


class IncidentPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def label(self) -> str:
        return {
            IncidentPriority.LOW: "Baja",
            IncidentPriority.MEDIUM: "Media",
            IncidentPriority.HIGH: "Alta",
            IncidentPriority.CRITICAL: "Crítica",
        }[self]
