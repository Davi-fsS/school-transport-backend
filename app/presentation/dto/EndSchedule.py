from pydantic import BaseModel

class EndSchedule(BaseModel):
    user_id: int
    schedule_id: int