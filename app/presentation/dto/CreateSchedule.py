from pydantic import BaseModel
from datetime import datetime

class CreateSchedule(BaseModel):
    schedule_name: str
    end_date: datetime
    user_id: int
    schedule_type: int