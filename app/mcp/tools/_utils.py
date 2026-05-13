import json
from dataclasses import asdict
from datetime import date, datetime
from enum import Enum
from uuid import UUID


def _default(obj: object) -> str:
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def serialize(data: object) -> str:
    if isinstance(data, list):
        return json.dumps([asdict(item) for item in data], default=_default)  # type: ignore[call-overload]
    return json.dumps(asdict(data), default=_default)  # type: ignore[call-overload]
