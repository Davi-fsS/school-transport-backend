from pydantic import BaseModel

class CreateVehiclePoint(BaseModel):
    user_id: int
    vehicle_id: int
    point_id: int