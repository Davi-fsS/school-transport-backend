from pydantic import BaseModel

class SaveCoordinate(BaseModel):
    lat: float
    lng: float
    alt: float | None
    user_id: int