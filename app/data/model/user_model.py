from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36))
    name = Column(String(255))
    email = Column(String(255))
    cpf = Column(String(11))
    cnh = Column(String(11))
    rg = Column(String(12))
    user_type_id = Column(Integer)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
