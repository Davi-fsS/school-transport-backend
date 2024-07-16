from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class PointModel(Base):
    __tablename__ = "point"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    address = Column(String(255))
    lat = Column(Double)
    lng = Column(Double)
    alt = Column(Double)
    city = Column(String(255))
    neighborhood = Column(String(255))
    state = Column(String(255))
    description = Column(String(255))
    point_type_id = Column(Integer)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
