from typing import List
from pydantic import BaseModel

from presentation.dto.Student import Student
from presentation.dto.User import User
from presentation.dto.Point import Point

class ScheduleCreated(BaseModel):
    points: List[Point]
    school: Point
    schedule_id: int
