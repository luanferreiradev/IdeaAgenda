from backend.Model.Calendar import Calendar
from backend.Dto.CalendarDto import CalendarDto
from typing import List

class CalendarMapper:
    @staticmethod
    def toModel(calendarDto: CalendarDto) -> Calendar:
        return Calendar(
            id=calendarDto.id,
            month=calendarDto.month,
            year=calendarDto.year,
            day=calendarDto.day
        )

    @staticmethod
    def toDto(calendar: Calendar) -> CalendarDto:
        return CalendarDto(
            id=calendar.id,
            month=calendar.month,
            year=calendar.year,
            day=calendar.day,
            tasks=[]  
        )

    @staticmethod
    def toModelList(calendarDtos: List[CalendarDto]) -> List[Calendar]:
        return [CalendarMapper.toModel(dto) for dto in calendarDtos]

    @staticmethod
    def toDtoList(calendars: List[Calendar]) -> List[CalendarDto]:
        return [CalendarMapper.toDto(calendar) for calendar in calendars]
