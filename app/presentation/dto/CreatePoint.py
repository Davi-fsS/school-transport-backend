from pydantic import BaseModel

class CreatePoint(BaseModel):
    name: str
    address: str
    city: str
    neighborhood: str
    state: str
    description: str
    point_type_id: int