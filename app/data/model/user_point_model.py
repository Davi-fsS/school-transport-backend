from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class UserPointModel(Base):
    __tablename__ = "user_point"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    point_id = Column(Integer)
    favorite = Column(Boolean)
    disabled = Column(Boolean, default=False)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
