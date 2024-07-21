from pydantic import BaseModel

class UpdateSchool(BaseModel):
    id: int
    name: str
    address: str
    city: str
    neighborhood: str
    state: str
    description: str