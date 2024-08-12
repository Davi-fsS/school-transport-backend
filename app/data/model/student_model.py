from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class StudentModel(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    year = Column(Integer)
    point_id = Column(Integer)
    code=Column(String(255))
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
