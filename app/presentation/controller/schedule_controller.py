from typing import List
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from presentation.dto.StartSchedule import StartSchedule
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
    
    def put_schedule_start(self, start: StartSchedule):
        return self.schedule_service.put_schedule_start(start)
    
    def put_schedule_point(self, schedule_point: PutSchedulePoint):
        return self.schedule_service.put_schedule_point(schedule_point)
    
    def put_schedule_end(self, schedule_id: int, user_id: int):
        return self.schedule_service.put_schedule_end(schedule_id, user_id)
