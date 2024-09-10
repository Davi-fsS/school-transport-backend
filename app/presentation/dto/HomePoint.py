from typing import List
from pydantic import BaseModel

from presentation.dto.Student import Student
from presentation.dto.User import User
from presentation.dto.Point import Point

class HomePoint(BaseModel):
    point: Point
    student: List[Student]
