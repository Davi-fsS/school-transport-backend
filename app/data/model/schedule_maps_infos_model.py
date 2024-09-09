from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class ScheduleMapsInfosModel(Base):
    __tablename__ = "schedule_maps_infos"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer)
    encoded_points = Column(String(255))
    legs_info = Column(String(255))
    eta = Column(String(255))
    creation_user = Column(Integer)
    change_date = Column(DateTime, nullable=True)
    change_user = Column(Integer, nullable=True)
