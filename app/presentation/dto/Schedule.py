from pydantic import BaseModel
from datetime import datetime

class Schedule(BaseModel):
    id: int
    name: str
    initial_date: datetime
    end_date: datetime | None
    real_initial_date: datetime | None
    real_end_date: datetime | None
    description: str
    schedule_type_id: int
    creation_user: int