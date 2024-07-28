from pydantic import BaseModel

class Point(BaseModel):
    id: int
    name: str
    address: str
    lat: float
    lng: float
    alt: float
    city: str
    neighborhood: str
    state: str
    description: str
    point_type_id: int

