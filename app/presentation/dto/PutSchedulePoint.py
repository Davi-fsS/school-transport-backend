from pydantic import BaseModel

class PutSchedulePoint(BaseModel):
    schedule_id: int
    point_id: int
    has_embarked: bool
    user_id: int

