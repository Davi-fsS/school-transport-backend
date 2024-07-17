from pydantic import BaseModel

class CreateStudent(BaseModel):
    name: str
    year: int
    responsible_id: int
    point_id: int