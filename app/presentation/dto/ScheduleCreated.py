from typing import List
from pydantic import BaseModel

from presentation.dto.HomePoint import HomePoint
from presentation.dto.Point import Point

class ScheduleCreated(BaseModel):
    points: List[HomePoint]
    school: Point
    schedule_id: int
