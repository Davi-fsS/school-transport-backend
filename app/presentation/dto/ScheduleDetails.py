from pydantic import BaseModel

from presentation.dto.Vehicle import Vehicle
from presentation.dto.User import User
from presentation.dto.Schedule import Schedule

class ScheduleDetails(BaseModel):
    schedule: Schedule
    driver: User
    vehicle: Vehicle