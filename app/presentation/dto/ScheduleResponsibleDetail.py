from typing import List
from pydantic import BaseModel

from presentation.dto.Point import Point
from presentation.dto.Vehicle import Vehicle
from presentation.dto.User import User
from presentation.dto.Student import Student

class ScheduleResponsibleDetail(BaseModel):
    students_in_home: List[Student]
    students_in_other_home: List[Student]
    driver: User
    point: Point
    vehicle: Vehicle