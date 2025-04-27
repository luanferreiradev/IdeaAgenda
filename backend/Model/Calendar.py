from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Calendar(Base):
    __tablename__ = "calendar"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer, index=True)
    year = Column(Integer, index=True)
    tasks = relationship("Task", back_populates="calendar")