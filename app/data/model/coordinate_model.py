from sqlalchemy import Column, Integer, String, DateTime, Double

from data.infrastructure.database import Base

class CoordinateModel(Base):
    __tablename__ = "coordinate"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Double)
    lng = Column(Double)
    alt = Column(Double, nullable=True)
    coordinate_type_id = Column(Integer)
    register_date = Column(DateTime)
    schedule_id = Column(Integer)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
