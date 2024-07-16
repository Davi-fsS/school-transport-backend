from pydantic import BaseModel

class CreateStudent(BaseModel):
    name: str
    age: int