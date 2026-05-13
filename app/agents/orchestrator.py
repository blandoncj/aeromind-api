from uuid import UUID

from google import genai
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.baggage_agent import BaggageAgent
from app.agents.base_agent import BaseAgent
from app.agents.flight_agent import FlightAgent
from app.agents.schemas import ChatOutput
from app.agents.security_agent import SecurityAgent
from app.agents.support_agent import SupportAgent
from app.infrastructure.config.settings import settings

_AGENTS: dict[str, type[BaseAgent]] = {
    "flight_agent": FlightAgent,
    "baggage_agent": BaggageAgent,
    "support_agent": SupportAgent,
    "security_agent": SecurityAgent,
}

_SYSTEM_PROMPT = """
Eres el orquestador del sistema multiagente de AeroMind.
Tu única tarea es clasificar la intención del usuario y seleccionar el agente correcto.

Agentes disponibles:
- flight_agent: consultas sobre vuelos, búsqueda de vuelos, estados, rutas
- baggage_agent: rastreo de equipaje, reporte de equipaje perdido o dañado
- support_agent: preguntas generales, políticas del aeropuerto, procedimientos, FAQs
- security_agent: restricciones de seguridad, objetos prohibidos, reglamentos

Responde ÚNICAMENTE con el nombre exacto del agente. Sin explicaciones ni texto adicional.
"""


class Orchestrator:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._client = genai.Client(api_key=settings.google_api_key)

    async def run(self, message: str, user_id: UUID | None = None) -> ChatOutput:
        response = await self._client.aio.models.generate_content(
            model=settings.google_llm_model,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM_PROMPT,
                temperature=0,
            ),
        )
        agent_name = (response.text or "support_agent").strip().lower()
        if agent_name not in _AGENTS:
            agent_name = "support_agent"

        agent = _AGENTS[agent_name](self._session, user_id)
        agent_response = await agent.run(message)

        return ChatOutput(response=agent_response, agent=agent_name)
