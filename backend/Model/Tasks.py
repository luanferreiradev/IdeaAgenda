from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import datetime
from backend.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completion_date = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, default=None)
    completed = Column(Boolean, default=False)