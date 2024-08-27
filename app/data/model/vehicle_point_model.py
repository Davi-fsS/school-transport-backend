from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class VehiclePointModel(Base):
    __tablename__ = "vehicle_point"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer)
    point_id = Column(Integer)
    disabled = Column(Boolean, default=False)
    code = Column(String(255))
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
