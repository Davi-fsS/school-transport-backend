from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class ScheduleModel(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    initial_date = Column(DateTime)
    end_date = Column(DateTime)
    real_initial_date = Column(DateTime, nullable=True)
    real_end_date = Column(DateTime, nullable=True)
    description = Column(String(255))
    schedule_type_id = Column(Integer)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
