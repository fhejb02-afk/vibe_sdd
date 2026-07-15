from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)


class TodoUpdate(BaseModel):
    completed: bool


class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    created_at: datetime


class TodoListResponse(BaseModel):
    todos: list[TodoOut]
    remaining_count: int
