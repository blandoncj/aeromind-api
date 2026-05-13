from abc import ABC, abstractmethod
from uuid import UUID

from google import genai
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.config.settings import settings

_MAX_TOOL_ROUNDS = 5


class BaseAgent(ABC):
    name: str
    system_prompt: str

    def __init__(self, session: AsyncSession, user_id: UUID | None = None) -> None:
        self._session = session
        self._user_id = user_id
        self._client = genai.Client(api_key=settings.google_api_key)

    @abstractmethod
    def _tool_declarations(self) -> list[types.FunctionDeclaration]: ...

    @abstractmethod
    async def _execute_tool(self, name: str, args: dict[str, str]) -> str: ...

    async def run(self, message: str) -> str:
        contents: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=message)])
        ]
        tool = types.Tool(function_declarations=self._tool_declarations())

        for _ in range(_MAX_TOOL_ROUNDS):
            response = await self._client.aio.models.generate_content(
                model=settings.google_llm_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=[tool],
                    system_instruction=self.system_prompt,
                ),
            )
            if not response.candidates:
                break
            candidate = response.candidates[0]
            if candidate.content is None:
                break
            contents.append(candidate.content)  # type: ignore[arg-type]

            parts = candidate.content.parts or []
            function_calls = [p for p in parts if p.function_call is not None]

            if not function_calls:
                return "".join(p.text for p in parts if p.text)

            responses: list[types.Part] = []
            for part in function_calls:
                fc = part.function_call
                assert fc is not None
                tool_result = await self._execute_tool(fc.name, dict(fc.args))  # type: ignore[arg-type]
                responses.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=fc.name,
                            response={"result": tool_result},
                        )
                    )
                )
            contents.append(types.Content(role="user", parts=responses))

        return "No pude procesar tu solicitud en este momento."
