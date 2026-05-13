from enum import StrEnum


class IncidentStatus(StrEnum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

    @property
    def label(self) -> str:
        return {
            IncidentStatus.OPEN: "Abierto",
            IncidentStatus.IN_PROGRESS: "En progreso",
            IncidentStatus.RESOLVED: "Resuelto",
            IncidentStatus.CLOSED: "Cerrado",
        }[self]
