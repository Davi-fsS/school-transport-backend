from sqlalchemy import Boolean, Column, Integer, String, DateTime, Double

from data.infrastructure.database import Base

class DeviceModel(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    disabled = Column(Boolean, default=False)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
