from pydantic import BaseModel

class CreateVehicle(BaseModel):
    plate: int
    vehicle_type_id: int
    color: str
    model: str
    year: str
    chassi: str
    renavam: str
    user_id: int