from business.service.user_service import UserService
from presentation.dto.Vehicle import Vehicle
from business.service.point_service import PointService
from data.repository.schedule_point_repository import SchedulePointRepository 

class SchedulePointService():
    schedule_point_repository: SchedulePointRepository
    point_service: PointService
    user_service: UserService

    def __init__(self):
        self.schedule_point_repository = SchedulePointRepository()
        self.point_service = PointService()
        self.user_service = UserService()

    def get_schedule_point_by_schedule_id(self, schedule_id: int):
        return self.schedule_point_repository.get_schedule_point_list_by_schedule_id(schedule_id)
    
    def get_points_by_schedule_id(self, schedule_id: int):
        schedule_point_list = self.schedule_point_repository.get_schedule_point_list_by_schedule_id(schedule_id)

        if(len(schedule_point_list) == 0):
            raise ValueError("Não existem pontos associados a esta viagem")
        
        point_list_ids = []

        for point in schedule_point_list:
            point_id = point.point_id
            point_list_ids.append(point_id)

        points_dto = self.point_service.get_point_list_by_user(point_list_ids)

        return points_dto