from typing import List
from pydantic import BaseModel
from datetime import datetime

from presentation.dto.SchedulePoint import SchedulePoint

class ScheduleHistoricDetails(BaseModel):
    id: int
    initial_date: datetime
    end_date: datetime | None
    real_initial_date: datetime | None
    real_end_date: datetime | None
    name: str
    schedule_type: str
    real_duration: datetime
    planned_duration: datetime
    points: List[SchedulePoint]