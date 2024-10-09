from typing import List
from pydantic import BaseModel

from presentation.dto.Schedule import Schedule
from presentation.dto.Coordinate import Coordinate

class ScheduleHistoric(BaseModel):
    schedule: Schedule
    coordinates: List[Coordinate]
