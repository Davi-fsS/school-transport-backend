from pydantic import BaseModel

class StudentAssociation(BaseModel):
    responsible_id: int
    student_id: int