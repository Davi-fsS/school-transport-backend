from pydantic import BaseModel
from presentation.dto.Point import Point
from presentation.dto.Student import Student
from presentation.dto.User import User

class StudentDetails(BaseModel):
    student: Student
    school: Point
    driver: User