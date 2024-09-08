from pydantic import BaseModel

class Student(BaseModel):
    id: int | None
    name: str
    year: int
    code: str
    point_id: int
    creation_user: int