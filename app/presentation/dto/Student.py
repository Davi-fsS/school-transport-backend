from pydantic import BaseModel

class Student(BaseModel):
    name: str
    year: int
    code: str
    creation_user: int