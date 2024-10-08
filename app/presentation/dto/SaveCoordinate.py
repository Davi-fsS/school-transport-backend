from pydantic import BaseModel

class SaveCoordinate(BaseModel):
    lat: float
    lng: float
    user_id: int
    schedule_id: int