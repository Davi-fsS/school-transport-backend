from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class ScheduleVehicleModel(Base):
    __tablename__ = "schedule_vehicle"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer)
    vehicle_id = Column(Integer)
    creation_user = Column(Integer)