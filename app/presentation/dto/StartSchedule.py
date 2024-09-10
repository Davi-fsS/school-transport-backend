from typing import List
from pydantic import BaseModel
from datetime import datetime

from presentation.dto.Point import Point

class StartSchedule(BaseModel):
    user_id: int
    schedule_id: int
    school_id: int
    end_date: datetime
    points: List[int]
    encoded_points: str
    legs_info: str
    eta: str