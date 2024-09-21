from pydantic import BaseModel
from datetime import datetime

class CreateParentNotification(BaseModel):
    user_id: int
    student_id: int
    inative_day: datetime
    period_id: int