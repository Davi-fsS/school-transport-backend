from pydantic import BaseModel

class CreateSchedule(BaseModel):
    vehicle_id: int
    school_id: int
    user_id: int
    schedule_type: int