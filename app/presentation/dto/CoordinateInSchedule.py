from pydantic import BaseModel
from presentation.dto.Coordinate import Coordinate
from presentation.dto.Schedule import Schedule
from typing import List

class CoordinateInSchedule(BaseModel):
    schedule: Schedule
    coordinates: List[Coordinate]

