from pydantic import BaseModel

class CreatePoint(BaseModel):
    address: str
    city: str
    neighborhood: str
    state: str