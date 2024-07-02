from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class UserTypeModel(Base):
    __tablename__ = "user_type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))