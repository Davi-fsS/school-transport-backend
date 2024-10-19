from pydantic import BaseModel

class SaveLoraCoordinate(BaseModel):
    lat: float
    lng: float
    device_code: str