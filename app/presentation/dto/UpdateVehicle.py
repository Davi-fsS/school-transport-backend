from pydantic import BaseModel

class UpdateVehicle(BaseModel):
    id: int
    plate: str
    model: str
    color: str
    year: str
    user_id: int