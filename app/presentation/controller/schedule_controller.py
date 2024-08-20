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
