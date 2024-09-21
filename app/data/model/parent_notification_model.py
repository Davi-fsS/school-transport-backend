from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class ParentNotificationModel(Base):
    __tablename__ = "parent_notification"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    student_id = Column(Integer)
    inative_day = Column(DateTime)
    parent_notification_period_id = Column(Integer)
    disabled = Column(Boolean)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
