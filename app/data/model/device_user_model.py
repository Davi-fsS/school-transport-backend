from sqlalchemy import Boolean, Column, Integer, String, DateTime, Double

from data.infrastructure.database import Base

class DeviceUserModel(Base):
    __tablename__ = "device_user"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)
    user_id = Column(Integer)
    disabled = Column(Boolean, default=False)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
