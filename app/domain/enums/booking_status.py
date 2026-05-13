from enum import StrEnum


class BookingStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    CHECKED_IN = "CHECKED_IN"
    BOARDED = "BOARDED"
    NO_SHOW = "NO_SHOW"

    @property
    def label(self) -> str:
        return {
            BookingStatus.CONFIRMED: "Confirmado",
            BookingStatus.CANCELLED: "Cancelado",
            BookingStatus.CHECKED_IN: "Registrado",
            BookingStatus.BOARDED: "Abordado",
            BookingStatus.NO_SHOW: "No presentado",
        }[self]
