from pydantic import BaseModel

class CreateStudent(BaseModel):
    id: int | None
    name: str
    year: int
    responsible_id: int
