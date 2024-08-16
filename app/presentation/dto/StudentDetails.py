from pydantic import BaseModel
from data.model.student_model import StudentModel
from data.model.user_model import UserModel
from presentation.dto.Point import Point

class StudentDetails(BaseModel):
    # student: StudentModel
    school: Point
    # driver: UserModel