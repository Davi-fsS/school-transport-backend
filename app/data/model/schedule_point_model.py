from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class SchedulePointModel(Base):
    __tablename__ = "schedule_point"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer)
    point_id = Column(Integer)
    creation_user = Column(Integer)