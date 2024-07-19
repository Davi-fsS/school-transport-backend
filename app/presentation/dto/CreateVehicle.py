from pydantic import BaseModel

class CreateVehicle(BaseModel):
    plate: str
    vehicle_type_id: int
    user_id: int