from pydantic import BaseModel, field_validator, field_serializer
from datetime import datetime
from typing import Any


class Task(BaseModel):
    uuid: str
    name: str
    created: datetime
    status: str
    progress: int
    last_error: str
    options: dict

    @field_validator('progress', mode='before')
    def float_to_int(cls, v):
        if isinstance(v, float):
            return int(v)
        return v


class PossibleOptions(BaseModel):
    name: str
    label: str
    default: Any
    type: str
    options: list[dict] = []


class TaskOptions(BaseModel):
    uuid: str
    options: dict
