from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class SchedulePointModel(Base):
    __tablename__ = "schedule_point"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer)
    point_id = Column(Integer)
    initial_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    real_initial_date = Column(DateTime, nullable=True)
    real_end_date = Column(DateTime, nullable=True)
    order = Column(Integer, nullable=True)
    description = Column(String)
    creation_user = Column(Integer)
