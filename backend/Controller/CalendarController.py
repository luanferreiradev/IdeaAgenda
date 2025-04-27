from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.Mapper.CalendarMapper import CalendarMapper
from backend.Dto.CalendarDto import CalendarDto
from backend.Model.Calendar import Calendar
from typing import List

router = APIRouter()

@router.get("/getAll", response_model=List[CalendarDto])
async def get_all_calendars(db: AsyncSession = Depends(get_db)):

    calendars = await db.query(Calendar).all()
    
    return CalendarMapper.toDtoList(calendars)

@router.get("/getById/{calendar_id}", response_model=CalendarDto)
async def get_calendar(calendar_id: int, db: AsyncSession = Depends(get_db)):
    calendar = await db.query(Calendar).filter(Calendar.id == calendar_id).first()
    
    return CalendarMapper.toDto(calendar)

@router.post("/post", response_model=CalendarDto)
async def create_calendar(calendar_dto: CalendarDto, db: AsyncSession = Depends(get_db)):
    calendar_model = CalendarMapper.toModel(calendar_dto)
    
    db.add(calendar_model)
    await db.commit()
    await db.refresh(calendar_model)
    
    return CalendarMapper.toDto(calendar_model)

@router.put("/calendar/{calendar_id}")
async def edit_calendar(calendar_dto: CalendarDto, db: AsyncSession = Depends(get_db)):
    calendar_model = CalendarMapper.toModel(calendar_dto)

    await db.commit()
    await db.refresh(calendar_model)

    return CalendarMapper.toDto(calendar_model)
    