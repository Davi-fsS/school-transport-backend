from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Double
from sqlalchemy.orm import relationship

from data.infrastructure.database import Base

class UserStudentModel(Base):
    __tablename__ = "user_student"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    student_id = Column(Integer)
    disabled=Column(Boolean, default=False)
    creation_user = Column(Integer)
    change_date = Column(DateTime)
    change_user = Column(Integer)
