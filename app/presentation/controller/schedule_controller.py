from typing import List
from presentation.dto.Point import Point
from business.service.schedule_service import ScheduleService
from presentation.dto.CreateSchedule import CreateSchedule

class ScheduleController():
    schedule_service: ScheduleService

    def __init__(self):
        self.schedule_service = ScheduleService()

    def get_schedule_details_by_schedule_id(self, schedule_id : int):
        return self.schedule_service.get_schedule_details_by_schedule_id(schedule_id)
    
    def create_schedule(self, schedule: CreateSchedule):
        return self.schedule_service.create_schedule(schedule)
    
    def put_schedule_start(self, schedule_id: int, points: List[int], school: Point, user_id: int):
        return self.schedule_service.put_schedule_start(schedule_id, points, school, user_id)
