from pydantic import BaseModel
from datetime import datetime

class Coordinate(BaseModel):
    lat: float
    lng: float
    coordinate_type_id: int
    schedule_id: int
    register_date: datetime
    creation_user: int