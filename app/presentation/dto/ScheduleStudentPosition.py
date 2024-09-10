from pydantic import BaseModel

class ScheduleStudentPosition(BaseModel):
    schedule_id : int
    user_id : int