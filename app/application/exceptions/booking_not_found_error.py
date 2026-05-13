from app.application.exceptions.application_error import ApplicationError


class BookingNotFoundError(ApplicationError):
    def __init__(self, reference: str) -> None:
        super().__init__(
            code="BOOKING_NOT_FOUND",
            message="Booking not found.",
            context={"booking_reference": reference}
        )
