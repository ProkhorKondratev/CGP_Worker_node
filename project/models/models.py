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


class TaskOptions(BaseModel):
    name: str
    value: Any
    default: Any
    type: str
    label: str
    description: str
    options: list[dict] = []
