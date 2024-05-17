from pydantic import BaseModel
from datetime import datetime
from typing import Any

class Task(BaseModel):
    uuid: str
    name: str
    created: datetime
    status: str
    progress: int
    last_error: str
    options: list[dict]


class PossibleOptions(BaseModel):
    name: str
    label: str
    default: Any
    type: str
    options: list[dict] = []

class TaskOptions(BaseModel):
    uuid: str
    options: dict
