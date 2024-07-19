from pydantic import BaseModel

class UpdateVehicle(BaseModel):
    id: int
    plate: str
    vehicle_type_id: int
    user_id: int