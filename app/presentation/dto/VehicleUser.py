from pydantic import BaseModel

class VehicleUser(BaseModel):
    id: int
    plate: str
    model: str | None
    color: str | None
    year: str | None
    user_id: int
    user_name: str