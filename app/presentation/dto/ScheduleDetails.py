from pydantic import BaseModel

from presentation.dto.HomePoint import HomePoint
from presentation.dto.Vehicle import Vehicle
from presentation.dto.User import User
from presentation.dto.Schedule import Schedule
from typing import List

class ScheduleDetails(BaseModel):
    schedule: Schedule
    driver: User
    vehicle: Vehicle
    points: List[HomePoint]