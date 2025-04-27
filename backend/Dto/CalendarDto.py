from pydantic import BaseModel
from typing import List
from backend.Dto.TasksDto import TaskDto

class CalendarDto(BaseModel):
    id: int
    month: int
    year: int
    day: int
    tasks: List[TaskDto]