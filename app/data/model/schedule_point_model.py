from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class SchedulePointModel(Base):
    __tablename__ = "schedule_point"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer)
    point_id = Column(Integer)
    initial_date = Column(DateTime)
    end_date = Column(DateTime)
    real_initial_date = Column(DateTime)
    real_end_date = Column(DateTime)
    order = Column(Integer)
    description = Column(String)
    creation_user = Column(Integer)