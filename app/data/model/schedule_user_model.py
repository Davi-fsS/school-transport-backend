from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class ScheduleUserModel(Base):
    __tablename__ = "schedule_user"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer)
    user_id = Column(Integer)
    creation_user = Column(Integer)