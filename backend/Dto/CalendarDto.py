from pydantic import BaseModel
from typing import List
from datetime import datetime
from backend.Dto.TasksDto import TaskDto
from uuid import UUID

class CalendarDto(BaseModel):
    id: UUID = None
    name: str
    created_at: datetime
    updated_at: datetime
    tasks: List[TaskDto]

    class Config:
        orm_mode = True