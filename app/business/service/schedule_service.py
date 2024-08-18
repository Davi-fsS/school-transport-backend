from presentation.dto.Schedule import Schedule
from data.repository.schedule_repository import ScheduleRepository

class ScheduleService():
    schedule_repository: ScheduleRepository

    def __init__(self):
        self.schedule_repository = ScheduleRepository()

    def get_schedule_by_id(self, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_by_id(schedule_id)

        schedule_dto = Schedule(id=schedule.id, name=schedule.name, initial_date=schedule.initial_date,
                                end_date=schedule.end_date, real_initial_date=schedule.real_initial_date,
                                real_end_date=schedule.real_end_date, description=schedule.description,
                                schedule_type_id=schedule.schedule_type_id, creation_user=schedule.creation_user)

        return schedule_dto