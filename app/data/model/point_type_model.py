from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class PointTypeModel(Base):
    __tablename__ = "point"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
