from typing import List
from pydantic import BaseModel

from presentation.dto.Point import Point
from presentation.dto.Schedule import Schedule
from presentation.dto.Coordinate import Coordinate

class ScheduleHistoricResponsible(BaseModel):
    schedule: Schedule
    points: List[Point]
    coordinates: List[Coordinate] | None
    coordinates_lora: List[Coordinate] | None
