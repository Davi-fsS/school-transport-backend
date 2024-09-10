from pydantic import BaseModel
from datetime import datetime

class UpdateStudentAddress(BaseModel):
    student_id: int
    user_id: int
    point_id: int = None