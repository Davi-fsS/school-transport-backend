from typing import List
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from presentation.dto.StartSchedule import StartSchedule
from presentation.dto.Point import Point
from business.service.schedule_service import ScheduleService
from presentation.dto.CreateSchedule import CreateSchedule
from datetime import date

class ScheduleController():
    schedule_service: ScheduleService

    def __init__(self):
        self.schedule_service = ScheduleService()

    def get_schedule_by_student(self, student_id : int, user_id: int):
        return self.schedule_service.get_schedule_by_student(student_id, user_id)
    
    def get_driver_schedule_details_by_schedule_id(self, schedule_id : int):
        return self.schedule_service.get_driver_schedule_details_by_schedule_id(schedule_id)
    
    def get_responsible_schedule_details_by_schedule_id(self, schedule_id : int, user_id: int):
        return self.schedule_service.get_responsible_schedule_details_by_schedule_id(schedule_id, user_id)
    
    def get_schedule_by_user(self, user_id: int):
        return self.schedule_service.get_schedule_by_user(user_id)
    
    def get_schedule_by_driver(self, user_id: int):
        return self.schedule_service.get_schedule_by_driver(user_id)
    
    def create_schedule(self, schedule: CreateSchedule):
        return self.schedule_service.create_schedule(schedule)
    
    def put_schedule_start(self, start: StartSchedule):
        return self.schedule_service.put_schedule_start(start)
    
    def put_schedule_point(self, schedule_point: PutSchedulePoint):
        return self.schedule_service.put_schedule_point(schedule_point)
    
    def put_schedule_end(self, schedule_id: int, user_id: int):
        return self.schedule_service.put_schedule_end(schedule_id, user_id)
    
    def get_schedule_student_position(self, schedule_id: int, user_id: int):
        return self.schedule_service.get_schedule_student_position(schedule_id, user_id)
    
    def get_schedule_driver_historic_by_date(self, date: str, user_id: int):
        return self.schedule_service.get_schedule_driver_historic_by_date(date, user_id)
    
    def get_schedule_responsible_historic_by_date(self, date: str, user_id: int):
        return self.schedule_service.get_schedule_responsible_historic_by_date(date, user_id)
    
    def get_schedule_driver_historic_details(self, schedule_id: int, user_id: int):
        return self.schedule_service.get_schedule_driver_historic_details(schedule_id, user_id)
    
    def get_schedule_maps_infos(self, schedule_id: int, user_id: int):
        return self.schedule_service.get_schedule_maps_infos(schedule_id, user_id)
