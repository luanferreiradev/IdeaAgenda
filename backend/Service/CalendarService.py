from sqlalchemy.ext.asyncio import AsyncSession
from backend.Mapper.CalendarMapper import CalendarMapper
from backend.Dto.CalendarDto import CalendarDto
from backend.Model.Calendar import Calendar
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def get_all_calendars(db: AsyncSession):
    result = await db.execute(select(Calendar))
    calendars = result.scalars().all()

    return [CalendarMapper.toDto(calendar) for calendar in calendars]

async def get_calendar(calendar_id: int, db: AsyncSession):
    result = await db.execute(select(Calendar).where(Calendar.id == calendar_id))
    calendar = result.scalar_one_or_none()
    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")

    return CalendarMapper.toDto(calendar)

async def create_calendar(calendar_dto: CalendarDto, db: AsyncSession):
    result  = await db.execute(select(Calendar).where(Calendar.id == calendar_dto.id))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Calendar with id {calendar_dto.id} already exists")


    calendar_model = CalendarMapper.toModel(calendar_dto)

    db.add(calendar_model)
    await db.commit()
    await db.refresh(calendar_model)

    result = await db.execute(
        select(Calendar).options(selectinload(Calendar.tasks)).where(Calendar.id == calendar_model.id)
    )
    calendar_with_tasks = result.scalar_one()

    return CalendarMapper.toDto(calendar_with_tasks)

async def edit_calendar(calendar_dto: CalendarDto, calendar_id: int, db: AsyncSession):
    result = await db.execute(select(Calendar).where(Calendar.id == calendar_id))
    calendar = result.scalar_one_or_none()

    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Calendar with id {calendar_id} not found"       )

    calendar.name = calendar_dto.name

    await db.commit()
    await db.refresh(calendar)

    result = await db.execute(
        select(Calendar).options(selectinload(Calendar.tasks)).where(Calendar.id == calendar.id)
    )
    calendar_with_tasks = result.scalar_one()

    return CalendarMapper.toDto(calendar_with_tasks)

async def delete_calendar(calendar_id: int, db: AsyncSession):
    result = await db.execute(select(Calendar).where(Calendar.id == calendar_id))
    calendar = result.scalar_one_or_none()

    if not calendar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")

    await db.delete(calendar)
    await db.commit()

    return {"Message": "Calendar deleted successfully", "Id": calendar_id}

"""async def merge_calendar(calendar_id: int, merge_id: int, db: AsyncSession):
    result = await db.execute("", )"""
