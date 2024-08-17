from pydantic import BaseModel

class Student(BaseModel):
    id: int | None
    name: str
    year: int
    code: str
    creation_user: int