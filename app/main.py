from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel

from app.api.routers import auth, baggage, bookings, chat, documents, flights, incidents
from app.application.exceptions.application_error import ApplicationError
from app.application.exceptions.baggage_not_found_error import BaggageNotFoundError
from app.application.exceptions.booking_not_found_error import BookingNotFoundError
from app.application.exceptions.flight_not_found_error import FlightNotFoundError
from app.application.exceptions.invalid_credentials_error import InvalidCredentialsError
from app.application.exceptions.user_already_exists_error import UserAlreadyExistsError
from app.domain.exceptions.domain_error import DomainError

app = FastAPI(title="AeroMind API")

app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(baggage.router)
app.include_router(incidents.router)
app.include_router(documents.router)
app.include_router(chat.router)

_NOT_FOUND_ERRORS = (FlightNotFoundError, BaggageNotFoundError, BookingNotFoundError)


@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request, exc: ApplicationError
) -> JSONResponse:
    if isinstance(exc, _NOT_FOUND_ERRORS):
        status_code = 404
    elif isinstance(exc, UserAlreadyExistsError):
        status_code = 409
    elif isinstance(exc, InvalidCredentialsError):
        status_code = 401
    else:
        status_code = 400

    return JSONResponse(
        status_code=status_code,
        content={"code": exc.code, "message": exc.message, "context": exc.context},
    )


@app.exception_handler(DomainError)
async def domain_error_handler(
    request: Request, exc: DomainError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"code": exc.code, "message": exc.message, "context": exc.context},
    )


class HealthResponse(BaseModel):
    status: str


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health")
def health() -> HealthResponse:
    return HealthResponse(status="ok")
