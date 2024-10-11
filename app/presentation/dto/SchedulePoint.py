from pydantic import BaseModel
from datetime import datetime

from presentation.dto.Point import Point

class SchedulePoint(BaseModel):
    id: int 
    point: Point | None
    planned_date: datetime | None
    real_date: datetime | None
    order: int
    schedule_id: int
    has_embarked: bool | None
    creation_user: int