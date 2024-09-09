from pydantic import BaseModel

class PutSchedulePoint(BaseModel):
    schedule_id: int
    schedule_point_id: int
    user_id: int

