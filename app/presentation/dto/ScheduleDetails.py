from pydantic import BaseModel

from presentation.dto.Vehicle import Vehicle
from presentation.dto.User import User
from presentation.dto.Schedule import Schedule
from presentation.dto.Point import Point
from typing import List

class ScheduleDetails(BaseModel):
    schedule: Schedule
    driver: User
    vehicle: Vehicle
    points: List[Point]