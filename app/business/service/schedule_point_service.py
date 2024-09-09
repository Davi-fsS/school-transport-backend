from typing import List
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

    def __init__(self):
        self.schedule_point_repository = SchedulePointRepository()
        self.point_service = PointService()
        self.user_service = UserService()
        self.student_service = StudentService()
        self.user_student_service = UserStudentService()

    def get_schedule_point_by_schedule_id(self, schedule_id: int):
        return self.schedule_point_repository.get_schedule_point_list_by_schedule_id(schedule_id)
    
    def get_points_by_schedule_id(self, schedule_id: int):
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

        student_list = []

        for point_dto in points_dto:
            for student_dto in students_points:
                if(student_dto.point_id == point_dto.id):
                    student_list.append(student_dto)

            home_point = HomePoint(point=point_dto, student=student_list)
            home_point_list.append(home_point)

        return home_point_list