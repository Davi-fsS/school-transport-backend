from pydantic import BaseModel

class CreateVehicle(BaseModel):
    plate: str
    vehicle_type_id: int
    color: str
    model: str
    year: str
    user_id: int