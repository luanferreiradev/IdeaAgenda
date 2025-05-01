from pydantic import BaseModel
from typing import List
from datetime import datetime
from backend.Dto.TasksDto import TaskDto

class CalendarDto(BaseModel):
    id: int

    name: str
    created_at: datetime
    updated_at: datetime

    tasks: List[TaskDto]