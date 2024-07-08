from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class UserPhoneModel(Base):
    __tablename__ = "user_phone"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    ddi = Column(String(4))
    ddd = Column(String(2))
    phone = Column(String(15))
    creation_user = Column(Integer)

    def __init__(self, user_id, ddi, ddd, phone, creation_user):
        self.user_id = user_id
        self.ddi = ddi
        self.ddd = ddd
        self.phone = phone
        self.creation_user = creation_user