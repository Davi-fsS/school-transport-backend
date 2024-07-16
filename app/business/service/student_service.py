from data.repository.student_repository import StudentRepository
from business.service.user_service import UserService
from business.service.point_service import PointService
from presentation.dto.CreateStudent import CreateStudent
from data.model.student_model import StudentModel

class StudentService():
    student_repository: StudentRepository
    user_service: UserService
    point_service: PointService

    def __init__(self):
        self.student_repository = StudentRepository()
        self.user_service = UserService()
        self.point_service = PointService()

    def create_student(self, student: CreateStudent):
        student_model = StudentModel(name=student.name, year=student.year, point_id=student.point_id, creation_user=2)

        if student.year <= 0:
            raise ValueError("Idade inválida")
        
        if self.user_service.get_user(student.responsible_id) is None:
            raise ValueError("Responsável inválido")
        
        if self.point_service.get_point(student.point_id) is None:
            raise ValueError("Ponto inválido")

        return self.student_repository.create_student(student_model)