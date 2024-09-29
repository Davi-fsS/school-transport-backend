from typing import List
from pydantic import BaseModel
from datetime import datetime

from presentation.dto.Student import Student
from presentation.dto.User import User
from presentation.dto.Point import Point

class ParentNotification(BaseModel):
    home: Point
    student: Student
    inative_day: datetime
    period: str
    canceled: bool
