from typing import List
from data.repository.student_repository import StudentRepository
from business.service.user_service import UserService
from business.service.point_service import PointService
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.UpdateStudent import UpdateStudent
from data.model.student_model import StudentModel
from business.service.user_student_service import UserStudentService

class StudentService():
    student_repository: StudentRepository
    user_service: UserService
    point_service: PointService
    user_student_service: UserStudentService

    def __init__(self):
        self.student_repository = StudentRepository()
        self.user_service = UserService()
        self.point_service = PointService()
        self.user_student_service = UserStudentService()

    def get_students_by_responsible(self, responsible_id: int):
        user_students_by_responsible_list = self.user_student_service.get_students_by_responsible(responsible_id=responsible_id)

        student_id_list = []
        for user_student in user_students_by_responsible_list:
            student_id_list.append(user_student.student_id)

        return self.student_repository.get_students_by_student_list(student_id_list=student_id_list)

    def create_student_list(self, student_list: List[CreateStudent]):
        self.validate_create_student_list(student_list=student_list)

        student_id_list = self.creating_students(student_list=student_list)

        self.user_student_service.create_user_student_list(student_id_list=student_id_list, user_id=student_list[0].responsible_id)
    
    def update_student(self, student: UpdateStudent):
        self.validate_update_student(student=student)

        return self.student_repository.update_student(student_update=student)
    
    def delete_student(self, student_id: int):
        self.user_student_service.delete_user_student(student_id=student_id)

        return self.student_repository.delete_student(student_id=student_id)

    def validate_create_student_list(self, student_list: List[CreateStudent]):
        for student in student_list:
            if len(student.name) == 0:
                raise ValueError("Nome inválido")
            
            if student.year <= 0:
                raise ValueError("Idade inválida")
            
            if self.user_service.get_user(student.responsible_id) is None:
                raise ValueError("Responsável inválido")

    def validate_update_student(self, student: UpdateStudent):
        if len(student.name) == 0:
            raise ValueError("Nome inválido")

        if student.year <= 0:
            raise ValueError("Idade inválida")

    def creating_students(self, student_list: List[CreateStudent]):
        student_model_list = []
        point = self.point_service.get_point_home_by_user_id(student_list[0].responsible_id)

        for student in student_list:
            if(student.id != None):
                student_model = StudentModel(name=student.name, year=student.year, point_id=point.id, creation_user=2)
                student_model_list.append(student_model)

        student_id = self.student_repository.create_student_list(student_model_list)

        return student_id