from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.application.use_cases.baggage.report_lost_baggage import (
    ReportLostBaggageUseCase)
from app.application.use_cases.baggage.track_baggage import TrackBaggageUseCase
from app.application.use_cases.bookings.get_booking import GetBookingUseCase
from app.application.use_cases.bookings.get_user_bookings import (
    GetUserBookingsUseCase)
from app.application.use_cases.flights.get_flight import GetFlightUseCase
from app.application.use_cases.flights.search_flights import SearchFlightsUseCase
from app.agents.orchestrator import Orchestrator
from app.application.use_cases.documents.ingest_document import IngestDocumentUseCase
from app.application.use_cases.documents.search_documents import SearchDocumentsUseCase
from app.application.use_cases.incidents.create_incident import (
    CreateIncidentUseCase)
from app.application.use_cases.incidents.get_incidents import GetIncidentsUseCase
from app.infrastructure.database.session import AsyncSessionFactory
from app.infrastructure.repositories.sqlalchemy_baggage_repository import (
    SqlAlchemyBaggageRepository)
from app.infrastructure.repositories.sqlalchemy_booking_repository import (
    SqlAlchemyBookingRepository)
from app.infrastructure.repositories.sqlalchemy_flight_repository import (
    SqlAlchemyFlightRepository)
from app.infrastructure.repositories.sqlalchemy_incident_repository import (
    SqlAlchemyIncidentRepository)
from app.infrastructure.repositories.sqlalchemy_document_repository import (
    SqlAlchemyDocumentRepository)
from app.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository)
from app.infrastructure.services.bcrypt_password_hasher import BcryptPasswordHasher
from app.infrastructure.services.gemini_embedding_service import GeminiEmbeddingService
from app.infrastructure.services.jwt_token_service import JwtTokenService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def _get_user_repo(session: SessionDep) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


def _get_flight_repo(session: SessionDep) -> SqlAlchemyFlightRepository:
    return SqlAlchemyFlightRepository(session)


def _get_booking_repo(session: SessionDep) -> SqlAlchemyBookingRepository:
    return SqlAlchemyBookingRepository(session)


def _get_baggage_repo(session: SessionDep) -> SqlAlchemyBaggageRepository:
    return SqlAlchemyBaggageRepository(session)


def _get_incident_repo(session: SessionDep) -> SqlAlchemyIncidentRepository:
    return SqlAlchemyIncidentRepository(session)


UserRepoDep = Annotated[SqlAlchemyUserRepository, Depends(_get_user_repo)]
FlightRepoDep = Annotated[SqlAlchemyFlightRepository, Depends(_get_flight_repo)]
BookingRepoDep = Annotated[SqlAlchemyBookingRepository, Depends(_get_booking_repo)]
BaggageRepoDep = Annotated[SqlAlchemyBaggageRepository, Depends(_get_baggage_repo)]
IncidentRepoDep = Annotated[SqlAlchemyIncidentRepository, Depends(_get_incident_repo)]


def get_login_use_case(
    user_repository: UserRepoDep,
    password_hasher: Annotated[BcryptPasswordHasher, Depends(BcryptPasswordHasher)],
    token_service: Annotated[JwtTokenService, Depends(JwtTokenService)],
) -> LoginUserUseCase:
    return LoginUserUseCase(user_repository, password_hasher, token_service)


def get_register_use_case(
    user_repository: UserRepoDep,
    password_hasher: Annotated[BcryptPasswordHasher, Depends(BcryptPasswordHasher)],
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository, password_hasher)


def get_search_flights_use_case(
    flight_repository: FlightRepoDep,
) -> SearchFlightsUseCase:
    return SearchFlightsUseCase(flight_repository)


def get_get_flight_use_case(
    flight_repository: FlightRepoDep,
) -> GetFlightUseCase:
    return GetFlightUseCase(flight_repository)


def get_get_booking_use_case(
    booking_repository: BookingRepoDep,
) -> GetBookingUseCase:
    return GetBookingUseCase(booking_repository)


def get_get_user_bookings_use_case(
    booking_repository: BookingRepoDep,
) -> GetUserBookingsUseCase:
    return GetUserBookingsUseCase(booking_repository)


def get_track_baggage_use_case(
    baggage_repository: BaggageRepoDep,
) -> TrackBaggageUseCase:
    return TrackBaggageUseCase(baggage_repository)


def get_report_lost_baggage_use_case(
    baggage_repository: BaggageRepoDep,
    incident_repository: IncidentRepoDep,
) -> ReportLostBaggageUseCase:
    return ReportLostBaggageUseCase(baggage_repository, incident_repository)


def get_create_incident_use_case(
    incident_repository: IncidentRepoDep,
) -> CreateIncidentUseCase:
    return CreateIncidentUseCase(incident_repository)


def get_get_incidents_use_case(
    incident_repository: IncidentRepoDep,
) -> GetIncidentsUseCase:
    return GetIncidentsUseCase(incident_repository)


def _get_document_repo(session: SessionDep) -> SqlAlchemyDocumentRepository:
    return SqlAlchemyDocumentRepository(session)


DocumentRepoDep = Annotated[SqlAlchemyDocumentRepository, Depends(_get_document_repo)]


def get_ingest_document_use_case(
    document_repository: DocumentRepoDep,
    embedding_service: Annotated[GeminiEmbeddingService, Depends(GeminiEmbeddingService)],
) -> IngestDocumentUseCase:
    return IngestDocumentUseCase(document_repository, embedding_service)


def get_orchestrator(session: SessionDep) -> Orchestrator:
    return Orchestrator(session)


def get_search_documents_use_case(
    document_repository: DocumentRepoDep,
    embedding_service: Annotated[GeminiEmbeddingService, Depends(GeminiEmbeddingService)],
) -> SearchDocumentsUseCase:
    return SearchDocumentsUseCase(document_repository, embedding_service)
