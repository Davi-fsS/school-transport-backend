from pydantic import BaseModel

class UpdateStudent(BaseModel):
    id: int
    name: str
    year: int