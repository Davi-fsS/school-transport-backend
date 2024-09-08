from typing import List
from pydantic import BaseModel

from presentation.dto.Point import Point

class StartSchedule(BaseModel):
    user_id: int
    schedule_id: int
    school: Point
    points: List[int]