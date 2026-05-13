from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.auth import CurrentUserDep
from app.api.dependencies import (
    get_get_booking_use_case,
    get_get_user_bookings_use_case,
)
from app.application.dtos.booking_dtos import GetBookingInput, GetUserBookingsInput
from app.application.use_cases.bookings.get_booking import GetBookingUseCase
from app.application.use_cases.bookings.get_user_bookings import GetUserBookingsUseCase
from app.domain.enums.booking_status import BookingStatus
from app.domain.enums.cabin_class import CabinClass

router = APIRouter(tags=["bookings"])


class BookingResponse(BaseModel):
    booking_id: UUID
    user_id: UUID
    flight_id: UUID
    booking_reference: str
    cabin_class: CabinClass
    status: BookingStatus
    seat_number: str | None
    created_at: datetime


@router.get("/bookings/{booking_reference}")
async def get_booking(
    booking_reference: str,
    use_case: Annotated[GetBookingUseCase, Depends(get_get_booking_use_case)],
    _: CurrentUserDep,
) -> BookingResponse:
    result = await use_case.execute(GetBookingInput(
        booking_reference=booking_reference,
    ))
    return BookingResponse(**vars(result))


@router.get("/users/{user_id}/bookings")
async def get_user_bookings(
    user_id: UUID,
    use_case: Annotated[GetUserBookingsUseCase, Depends(get_get_user_bookings_use_case)],
    _: CurrentUserDep,
) -> list[BookingResponse]:
    results = await use_case.execute(GetUserBookingsInput(user_id=user_id))
    return [BookingResponse(**vars(b)) for b in results]
