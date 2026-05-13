import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dtos.booking_dtos import BookingOutput, GetBookingInput
from app.application.exceptions.booking_not_found_error import BookingNotFoundError
from app.application.use_cases.bookings.get_booking import GetBookingUseCase
from app.domain.enums.booking_status import BookingStatus
from app.domain.enums.cabin_class import CabinClass


def _make_booking(reference: str = "ABC123") -> MagicMock:
    booking = MagicMock()
    booking.booking_id = uuid4()
    booking.user_id = uuid4()
    booking.flight_id = uuid4()
    booking.booking_reference.value = reference
    booking.cabin_class = CabinClass.ECONOMY
    booking.status = BookingStatus.CONFIRMED
    booking.seat_number = None
    booking.created_at = datetime(2026, 5, 1, tzinfo=timezone.utc)
    return booking


class TestGetBookingUseCase:
    def test_returns_booking_output(self) -> None:
        booking = _make_booking("ABC123")
        repo = AsyncMock()
        repo.find_by_reference.return_value = booking

        result = asyncio.run(GetBookingUseCase(repo).execute(GetBookingInput("ABC123")))

        assert isinstance(result, BookingOutput)
        assert result.booking_reference == "ABC123"
        assert result.cabin_class == CabinClass.ECONOMY
        assert result.status == BookingStatus.CONFIRMED
        assert result.seat_number is None

    def test_raises_when_booking_not_found(self) -> None:
        repo = AsyncMock()
        repo.find_by_reference.return_value = None

        with pytest.raises(BookingNotFoundError) as exc_info:
            asyncio.run(GetBookingUseCase(repo).execute(GetBookingInput("ZZZ999")))

        assert exc_info.value.code == "BOOKING_NOT_FOUND"

    def test_normalizes_reference_to_uppercase(self) -> None:
        booking = _make_booking("ABC123")
        repo = AsyncMock()
        repo.find_by_reference.return_value = booking

        asyncio.run(GetBookingUseCase(repo).execute(GetBookingInput("abc123")))

        called_ref = repo.find_by_reference.call_args[0][0]
        assert called_ref.value == "ABC123"

    def test_maps_seat_number_when_present(self) -> None:
        booking = _make_booking()
        seat = MagicMock()
        seat.value = "12A"
        booking.seat_number = seat
        repo = AsyncMock()
        repo.find_by_reference.return_value = booking

        result = asyncio.run(GetBookingUseCase(repo).execute(GetBookingInput("ABC123")))

        assert result.seat_number == "12A"


class TestGetUserBookingsUseCase:
    def test_returns_all_user_bookings(self) -> None:
        from app.application.dtos.booking_dtos import GetUserBookingsInput
        from app.application.use_cases.bookings.get_user_bookings import GetUserBookingsUseCase

        user_id = uuid4()
        repo = AsyncMock()
        repo.find_by_user_id.return_value = [_make_booking("ABC123"), _make_booking("XYZ789")]

        result = asyncio.run(GetUserBookingsUseCase(repo).execute(GetUserBookingsInput(user_id)))

        assert len(result) == 2
        repo.find_by_user_id.assert_called_once_with(user_id)

    def test_returns_empty_when_no_bookings(self) -> None:
        from app.application.dtos.booking_dtos import GetUserBookingsInput
        from app.application.use_cases.bookings.get_user_bookings import GetUserBookingsUseCase

        repo = AsyncMock()
        repo.find_by_user_id.return_value = []

        result = asyncio.run(GetUserBookingsUseCase(repo).execute(GetUserBookingsInput(uuid4())))

        assert result == []
