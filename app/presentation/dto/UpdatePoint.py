from pydantic import BaseModel

class UpdatePoint(BaseModel):
    id: int
    name: str
    address: str
    city: str
    neighborhood: str
    state: str
    description: str
    point_type_id: int