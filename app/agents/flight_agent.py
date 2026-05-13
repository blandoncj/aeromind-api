from datetime import date
from uuid import UUID

from google.genai import types

from app.agents.base_agent import BaseAgent
from app.application.dtos.flight_dtos import GetFlightInput, SearchFlightsInput
from app.application.use_cases.flights.get_flight import GetFlightUseCase
from app.application.use_cases.flights.search_flights import SearchFlightsUseCase
from app.infrastructure.repositories.sqlalchemy_flight_repository import (
    SqlAlchemyFlightRepository,
)
from app.mcp.tools._utils import serialize


class FlightAgent(BaseAgent):
    name = "flight_agent"
    system_prompt = (
        "Eres un asistente especializado en vuelos del aeropuerto AeroMind. "
        "Ayudas a los pasajeros a buscar vuelos disponibles y consultar detalles de vuelos. "
        "Usa las herramientas disponibles para obtener información real. "
        "Responde siempre en español de forma clara y amigable."
    )

    def _tool_declarations(self) -> list[types.FunctionDeclaration]:
        return [
            types.FunctionDeclaration(
                name="search_flights",
                description="Busca vuelos disponibles entre dos aeropuertos en una fecha",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "origin": types.Schema(type="STRING", description="Código IATA del origen (ej: BOG, MIA, JFK)"),
                        "destination": types.Schema(type="STRING", description="Código IATA del destino"),
                        "departure_date": types.Schema(type="STRING", description="Fecha de salida YYYY-MM-DD"),
                    },
                    required=["origin", "destination", "departure_date"],
                ),
            ),
            types.FunctionDeclaration(
                name="get_flight",
                description="Obtiene los detalles de un vuelo por su ID",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "flight_id": types.Schema(type="STRING", description="UUID del vuelo"),
                    },
                    required=["flight_id"],
                ),
            ),
        ]

    async def _execute_tool(self, name: str, args: dict[str, str]) -> str:
        repo = SqlAlchemyFlightRepository(self._session)
        if name == "search_flights":
            results = await SearchFlightsUseCase(repo).execute(
                SearchFlightsInput(
                    origin=args["origin"],
                    destination=args["destination"],
                    departure_date=date.fromisoformat(args["departure_date"]),
                )
            )
            return serialize(results)
        if name == "get_flight":
            result = await GetFlightUseCase(repo).execute(
                GetFlightInput(flight_id=UUID(args["flight_id"]))
            )
            return serialize(result)
        return "Herramienta no encontrada."
