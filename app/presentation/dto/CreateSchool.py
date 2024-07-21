from pydantic import BaseModel

class CreateSchool(BaseModel):
    name: str
    address: str
    city: str
    neighborhood: str
    state: str
    description: str