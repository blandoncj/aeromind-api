from dataclasses import dataclass


@dataclass(frozen=True)
class ChatOutput:
    response: str
    agent: str
