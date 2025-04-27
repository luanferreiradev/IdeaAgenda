from backend.Model.Tasks import Task
from backend.Dto.TasksDto import TaskDto
from typing import List, Optional
from datetime import datetime

class TasksMapper:
    @staticmethod
    def toModel(taskDto: TaskDto) -> Task:
        return Task(
            id=taskDto.id,
            title=taskDto.title,
            description=taskDto.description,
            completion_date=taskDto.completion_date,
            created_at=taskDto.created_at or datetime.utcnow(),
            updated_at=taskDto.updated_at or datetime.utcnow(),
            completed_at=taskDto.completed_at,
            completed=taskDto.completed
        )

    @staticmethod
    def toDto(task: Task) -> TaskDto:
        return TaskDto(
            id=task.id,
            title=task.title,
            description=task.description,
            completion_date=task.completion_date,
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            completed=task.completed
        )

    @staticmethod
    def toModelList(taskDtos: List[TaskDto]) -> List[Task]:
        return [TasksMapper.toModel(dto) for dto in taskDtos]

    @staticmethod
    def toDtoList(tasks: List[Task]) -> List[TaskDto]:
        return [TasksMapper.toDto(task) for task in tasks]
