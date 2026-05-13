from enum import StrEnum


class FlightStatus(StrEnum):
    SCHEDULED = "SCHEDULED"
    BOARDING = "BOARDING"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"
    DELAYED = "DELAYED"
    CANCELLED = "CANCELLED"

    @property
    def label(self) -> str:
        return {
            FlightStatus.SCHEDULED: "Programado",
            FlightStatus.BOARDING: "Abordando",
            FlightStatus.DEPARTED: "Despegado",
            FlightStatus.ARRIVED: "Aterrizado",
            FlightStatus.DELAYED: "Retrasado",
            FlightStatus.CANCELLED: "Cancelado",
        }[self]
