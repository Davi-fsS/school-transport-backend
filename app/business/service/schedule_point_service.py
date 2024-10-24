from typing import List
from datetime import date
from presentation.dto.SchedulePoint import SchedulePoint
from data.repository.schedule_repository import ScheduleRepository
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from business.service.user_student_service import UserStudentService
from presentation.dto.Point import Point
from presentation.dto.HomePoint import HomePoint
from business.service.student_service import StudentService
from business.service.user_service import UserService
from business.service.point_service import PointService
from data.repository.schedule_point_repository import SchedulePointRepository 

class SchedulePointService():
    schedule_point_repository: SchedulePointRepository
    point_service: PointService
    user_service: UserService
    student_service: StudentService
    user_student_service: UserStudentService
    schedule_repository: ScheduleRepository

    def __init__(self):
        self.schedule_point_repository = SchedulePointRepository()
        self.point_service = PointService()
        self.user_service = UserService()
        self.student_service = StudentService()
        self.user_student_service = UserStudentService()
        self.schedule_repository = ScheduleRepository()

    def get_schedule_point_by_schedule_id(self, schedule_id: int):
        return self.schedule_point_repository.get_schedule_point_list_by_schedule_id(schedule_id)

    def get_points_by_schedule_id(self, schedule_id: int) -> List[HomePoint]:
        home_point_list: List[HomePoint] = []

        schedule_point_list = self.schedule_point_repository.get_schedule_point_list_by_schedule_id(schedule_id)

        if(len(schedule_point_list) == 0):
            raise ValueError("Não existem pontos associados a esta viagem")
        
        point_list_ids = []

        for point in schedule_point_list:
            point_id = point.point_id
            point_list_ids.append(point_id)

        points_dto : List[Point] = self.point_service.get_point_list_by_user(point_list_ids)

        students_points = self.student_service.get_students_by_point_list(point_list_ids)

        student_id_list = []

        for student in students_points:
            student_id_list.append(student.id)

        for point_dto in points_dto:
            schedule_point = list(filter(lambda schedPoint: schedPoint.point_id == point_dto.id, schedule_point_list))[0]

            schedule_point_dto = SchedulePoint(id=schedule_point.id, point=point_dto, planned_date=schedule_point.planned_date,
                                               real_date=schedule_point.real_date, order=schedule_point.order, schedule_id=schedule_point.schedule_id,
                                               has_embarked=schedule_point.has_embarked, creation_user=schedule_point.creation_user)

            if(schedule_point_dto.has_embarked is None):
                student_list = []
                for student_dto in students_points:
                    if(student_dto.point_id == point_dto.id):
                        student_list.append(student_dto)

                home_point = HomePoint(point=point_dto, student=student_list, status=schedule_point_dto)
                home_point_list.append(home_point)

        return sorted(home_point_list, key=lambda home_point: home_point.status.order)
    
    def get_schedule_point_by_id(self, id: int):
        return self.schedule_point_repository.get_schedule_point_by_id(id)
    
    def get_current_schedule_point_by_schedule_id(self, schedule_id: int):
        return self.schedule_point_repository.get_current_schedule_point_by_schedule_id(schedule_id)
    
    def get_schedule_point_by_point_id(self, schedule_id: int, point_id: int):
        return self.schedule_point_repository.get_schedule_point_by_point_id(schedule_id, point_id)
    
    def get_schedule_point_list_by_point_list_date(self, point_list: List[int], date: date):
        return self.schedule_point_repository.get_schedule_point_by_point_list_date(point_list, date)
    
    def get_last_schedule_point(self, schedule_id: int):
        return self.schedule_point_repository.get_last_schedule_point(schedule_id)

    def get_current_schedule_list_by_point_list(self, point_list: List[int]):
        schedules_points = self.schedule_point_repository.get_schedule_point_by_point_list(point_list)

        if len(schedules_points) == 0: 
            return []
        
        schedule_ids = []
        for schedule_point in schedules_points:
            schedule_ids.append(schedule_point.schedule_id)

        current_schedules = self.schedule_repository.get_schedule_list_in_progress_by_list(schedule_ids)

        if len(current_schedules) == 0:
            return []

        return current_schedules

    def put_schedule_point(self, schedule_id: int, point_id: int, user_id: int, has_embarked: bool):
        return self.schedule_point_repository.put_schedule_point(schedule_id, point_id, user_id, has_embarked)