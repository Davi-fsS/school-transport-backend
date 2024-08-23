from pydantic import BaseModel

class Vehicle(BaseModel):
    id: int
    plate: str
    vehicle_type_id: int
    color: str
    model: str
    year: str
    code: str

