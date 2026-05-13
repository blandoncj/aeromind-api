from google.genai import types

from app.agents.base_agent import BaseAgent
from app.application.dtos.baggage_dtos import ReportLostBaggageInput, TrackBaggageInput
from app.application.use_cases.baggage.report_lost_baggage import ReportLostBaggageUseCase
from app.application.use_cases.baggage.track_baggage import TrackBaggageUseCase
from app.infrastructure.repositories.sqlalchemy_baggage_repository import (
    SqlAlchemyBaggageRepository,
)
from app.infrastructure.repositories.sqlalchemy_incident_repository import (
    SqlAlchemyIncidentRepository,
)
from app.mcp.tools._utils import serialize


class BaggageAgent(BaseAgent):
    name = "baggage_agent"
    system_prompt = (
        "Eres un asistente especializado en equipaje del aeropuerto AeroMind. "
        "Ayudas a los pasajeros a rastrear su equipaje y reportar pérdidas. "
        "Usa las herramientas disponibles para obtener información real. "
        "Responde siempre en español de forma clara y empática."
    )

    def _tool_declarations(self) -> list[types.FunctionDeclaration]:
        return [
            types.FunctionDeclaration(
                name="track_baggage",
                description="Rastrea el estado actual del equipaje por su número de etiqueta",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "tag": types.Schema(type="STRING", description="Número de etiqueta del equipaje"),
                    },
                    required=["tag"],
                ),
            ),
            types.FunctionDeclaration(
                name="report_lost_baggage",
                description="Reporta un equipaje como perdido y crea un incidente automáticamente",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "tag": types.Schema(type="STRING", description="Número de etiqueta del equipaje"),
                        "description": types.Schema(type="STRING", description="Descripción opcional de la situación"),
                    },
                    required=["tag"],
                ),
            ),
        ]

    async def _execute_tool(self, name: str, args: dict[str, str]) -> str:
        baggage_repo = SqlAlchemyBaggageRepository(self._session)
        if name == "track_baggage":
            track_result = await TrackBaggageUseCase(baggage_repo).execute(
                TrackBaggageInput(tag=args["tag"])
            )
            return serialize(track_result)
        if name == "report_lost_baggage":
            if self._user_id is None:
                return "Se requiere autenticación para reportar equipaje perdido."
            incident_repo = SqlAlchemyIncidentRepository(self._session)
            report_result = await ReportLostBaggageUseCase(baggage_repo, incident_repo).execute(
                ReportLostBaggageInput(
                    tag=args["tag"],
                    reported_by=self._user_id,
                    description=args.get("description"),
                )
            )
            return serialize(report_result)
        return "Herramienta no encontrada."
