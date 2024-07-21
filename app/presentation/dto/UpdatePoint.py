from pydantic import BaseModel

class UpdatePoint(BaseModel):
    id: int
    address: str
    city: str
    neighborhood: str
    state: str