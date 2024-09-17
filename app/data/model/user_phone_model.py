from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class UserPhoneModel(Base):
    __tablename__ = "user_phone"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    ddi = Column(String(4), nullable=True)
    ddd = Column(String(2), nullable=True)
    phone = Column(String(15), nullable=True)
    disabled = Column(Boolean, default=False)
    creation_user = Column(Integer)
    change_date = Column(DateTime, nullable=True)
    change_user = Column(Integer, nullable=True)