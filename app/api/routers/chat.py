from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.orchestrator import Orchestrator
from app.api.auth import CurrentUserDep
from app.api.dependencies import get_orchestrator

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    agent: str


@router.post("")
async def chat(
    body: ChatRequest,
    orchestrator: Annotated[Orchestrator, Depends(get_orchestrator)],
    current_user: CurrentUserDep,
) -> ChatResponse:
    result = await orchestrator.run(body.message, current_user.user_id)
    return ChatResponse(**vars(result))
