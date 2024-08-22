from pydantic import BaseModel

class VehiclePointAssociation(BaseModel):
    vehicle_id: int
    point_id: int