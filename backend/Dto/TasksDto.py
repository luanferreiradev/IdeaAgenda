from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskDto(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completion_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    completed: bool = False