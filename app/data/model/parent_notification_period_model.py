from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class ParentNotificationPeriodModel(Base):
    __tablename__ = "parent_notification_period"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    schedule_type_id = Column(Integer)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
