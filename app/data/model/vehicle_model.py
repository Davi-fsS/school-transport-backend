from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class VehicleModel(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(7))
    vehicle_type_id = Column(Integer)
    color = Column(String(255), nullable=True)
    model = Column(String(255), nullable=True)
    year = Column(String(255), nullable=True)
    chassi = Column(String(255), nullable=True)
    renavam = Column(String(255), nullable=True)
    user_id = Column(Integer)
    code = Column(String(255), nullable=True)
    point_id = Column(Integer)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
