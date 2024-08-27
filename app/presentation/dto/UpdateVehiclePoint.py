from pydantic import BaseModel

class UpdateVehiclePoint(BaseModel):
    vehicle_point_id: int
    user_id: int
    vehicle_id: int
    point_id: int