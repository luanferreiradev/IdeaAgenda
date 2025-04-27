from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.Mapper.TasksMapper import TasksMapper
from backend.Dto.TasksDto import TaskDto
from backend.Model.Tasks import Task
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/post", response_model=TaskDto)
async def create_task(task_dto: TaskDto, db: AsyncSession = Depends(get_db)):
    task_model = TasksMapper.toModel(task_dto)

    db.add(task_model)
    await db.commit()
    await db.refresh(task_model)

    return TasksMapper.toDto(task_model)

@router.get("/get", response_model=List[TaskDto])
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await db.query(Task).all()

    return TasksMapper.toDtoList(tasks)

@router.get("/getById/{task_id}", response_model=TaskDto)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TasksMapper.toDto(task)

@router.put("/edit/{task_id}", response_model=TaskDto)
async def update_task(task_id: int, task_dto: TaskDto, db: AsyncSession = Depends(get_db)):
    task = await db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_dto.title
    task.description = task_dto.description
    task.completion_date = task_dto.completion_date
    task.completed = task_dto.completed
    task.completed_at = task_dto.completed_at
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return TasksMapper.toDto(task)

@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    
    return {"message": "Task deleted successfully"}
