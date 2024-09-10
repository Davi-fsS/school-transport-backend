from typing import List
from presentation.dto.Point import Point
from data.repository.student_repository import StudentRepository
from business.service.user_service import UserService
from business.service.point_service import PointService
from business.service.user_point_service import UserPointService
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.StudentAssociation import StudentAssociation
from presentation.dto.UpdateStudent import UpdateStudent
from presentation.dto.StudentDetails import StudentDetails
from presentation.dto.User import User
from presentation.dto.Student import Student
from data.model.student_model import StudentModel
from business.service.user_student_service import UserStudentService
from business.service.user_phone_service import UserPhoneService

class StudentService():
    student_repository: StudentRepository
    user_service: UserService
    point_service: PointService
    user_student_service: UserStudentService
    user_point_service: UserPointService
    user_phone_service: UserPhoneService

    def __init__(self):
        self.student_repository = StudentRepository()
        self.user_service = UserService()
        self.point_service = PointService()
        self.user_student_service = UserStudentService()
        self.user_point_service = UserPointService()
        self.user_phone_service = UserPhoneService()

    def get_students_by_responsible(self, responsible_id: int):
        user_students_by_responsible_list = self.user_student_service.get_students_by_responsible(responsible_id=responsible_id)

        student_id_list = []
        for user_student in user_students_by_responsible_list:
            student_id_list.append(user_student.student_id)

        return self.student_repository.get_students_by_student_list(student_id_list=student_id_list)
    
    def get_students_by_list(self, student_id_list: List[int]):
        return self.student_repository.get_students_by_student_list(student_id_list)
    
    def get_student_by_code(self, code: str):
        student = self.student_repository.get_student_by_code(code)

        if(student is None):
            raise ValueError("Aluno não encontrado")
        
        student_details = self.get_student_details(student.id)
        
        return student_details
    
    def get_students_by_point_list(self, point_list: List[int]) -> List[Student]:
        students_dto : List[Student] = []
        students = self.student_repository.get_students_by_point_list(point_list)

        for student in students:
            students_dto.append(Student(id=student.id, name=student.name, year=student.year, code=student.code, creation_user=student.creation_user, point_id=student.point_id))

        return students_dto
    
    def get_student_details(self, student_id: int):
        student = self.student_repository.get_student(student_id)

        if(student is None):
            raise ValueError("Aluno não encontrado")
        
        student_dto = Student(id=student.id, point_id=student.point_id, name=student.name, year=student.year, code=student.code, creation_user=student.creation_user)
        
        student_driver = self.get_student_driver(student_id)

        if(student_driver is None):
            raise ValueError("Aluno não possui motorista")

        driver_phone = self.user_phone_service.get_user_phone_list(student_driver.id)

        student_driver_dto = User(id=student_driver.id, uuid=student_driver.uuid, name=student_driver.name,
                                  email=student_driver.email, cpf=student_driver.cpf, cnh=student_driver.cnh,
                                  rg=student_driver.rg, user_type_id=student_driver.user_type_id, code=student_driver.code, phones=driver_phone)

        student_school_dto = self.get_student_school(student_driver.id)

        student_home = self.point_service.get_point(student.point_id)

        student_home_dto = Point(id=student_home.id, name=student_home.name, address=student_home.address,
                                 lat=student_home.lat, lng=student_home.lng, alt=student_home.alt,
                                 city=student_home.city, neighborhood=student_home.neighborhood, state=student_home.state,
                                 description=student_home.description, point_type_id=student_home.point_type_id)

        if(student_school_dto is None):
            raise ValueError("Aluno não possui escola")
        
        student_details_dto = StudentDetails(school=student_school_dto, student=student_dto, point=student_home_dto, driver=student_driver_dto)
        
        return student_details_dto

    def get_student_driver(self, student_id: int):
        user_student_list = self.user_student_service.get_user_students_by_student_id(student_id)

        user_id_list = []
        for user_student in user_student_list:
            user_id = user_student.user_id
            user_id_list.append(user_id)

        users = self.user_service.get_user_list_by_list(user_id_list)

        for user in users:
            if(user.user_type_id != 3):
                return user
            
    def get_student_school(self, driver_id: int):
        user_points = self.user_point_service.get_user_point_list(driver_id)

        point_id_list = []
        for user_point in user_points:
            point_id = user_point.point_id
            point_id_list.append(point_id)

        points = self.point_service.get_point_list_by_user(point_id_list)

        for point in points:
            if(point.point_type_id == 2):
                return point

    def get_all_student_homes(self, student_id: int, user_id: int):
        user = self.user_service.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if(user.user_type_id == 2):
            raise ValueError("Usuário não é um responsável")
        
        student = self.student_repository.get_student(student_id)

        if(student.creation_user != user_id):
            raise ValueError("Usuário não autorizado")
        
        responsibles = self.user_student_service.get_responsibles_by_student_id(student.id)

        responsibles_ids = []
        for responsible in responsibles:
            responsibles_ids.append(responsible.id)

        responsible_points = self.user_point_service.get_user_point_list_by_user_list(responsibles_ids)

        responsible_points_ids = []
        for responsible_point in responsible_points:
            responsible_points_ids.append(responsible_point.point_id)

        return self.point_service.get_point_home_list_by_user(responsible_points_ids)

    def create_association_student_responsible(self, association: StudentAssociation):
        self.validating_association(association)

        return self.user_student_service.create_user_student(user_id=association.responsible_id, student_id=association.student_id)

    def disassociation_student_responsible(self, disassociation: StudentAssociation):
        self.validating_disassociation(disassociation)

        return self.user_student_service.delete_user_student(student_id=disassociation.student_id, responsible_id=disassociation.responsible_id)

    def create_student(self, student: CreateStudent):
        self.validate_create_student(student)

        student_id = self.creating_student(student)

        self.user_student_service.create_user_student(student_id=student_id, user_id=student.responsible_id)

        driver = self.user_service.get_user(student.driver_id)

        self.user_student_service.create_user_student(student_id=student_id, user_id=driver.id)

    def create_student_list(self, student_list: List[CreateStudent]):
        self.validate_create_student_list(student_list=student_list)

        student_id_list = self.creating_students(student_list=student_list)

        self.user_student_service.create_user_student_list(student_id_list=student_id_list, user_id=student_list[0].responsible_id)
    
    def update_student(self, student: UpdateStudent):
        self.validate_update_student(student=student)

        return self.student_repository.update_student(student_update=student)
    
    def update_student_address(self, student_id: int, user_id: int):
        user = self.user_service.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")

        if user.user_type_id == 2:
            raise ValueError("Este usuário não é um responsável")

        point = self.point_service.get_point_home_by_user_id(user.id)

        if point is None:
            raise ValueError("Este usuário não possuí um endereço")

        return self.student_repository.update_student_address(student_id, point.id, user_id)
    
    def delete_student(self, student_id: int):
        self.user_student_service.delete_user_student_by_student_id(student_id=student_id)

        return self.student_repository.delete_student(student_id=student_id)

    def validate_create_student_list(self, student_list: List[CreateStudent]):
        for student in student_list:
            if len(student.name) == 0:
                raise ValueError("Nome inválido")
            
            if student.year <= 0:
                raise ValueError("Idade inválida")
            
            if self.user_service.get_user(student.responsible_id) is None:
                raise ValueError("Responsável inválido")
    
    def validate_create_student(self, student: CreateStudent):
        if len(student.name) == 0:
            raise ValueError("Nome inválido")
        
        if student.year <= 0:
            raise ValueError("Idade inválida")
        
        if self.user_service.get_user(student.responsible_id) is None:
            raise ValueError("Responsável inválido")

    def validate_update_student(self, student: UpdateStudent):
        student_db = self.student_repository.get_student(student_id=student.id)

        if(student_db is None):
            raise ValueError("Aluno não existe")
        
        if len(student.name) == 0:
            raise ValueError("Nome inválido")

        if student.year <= 0:
            raise ValueError("Idade inválida")

    def creating_student(self, student: CreateStudent):
        point = self.point_service.get_point_home_by_user_id(student.responsible_id)
        responsible_data = self.user_service.get_user(student.responsible_id)

        student_code = self.generate_student_code(student.name, responsible_data.uuid)
        student_model = StudentModel(name=student.name, year=student.year, code=student_code, point_id=point.id, creation_user=student.responsible_id)

        student_id = self.student_repository.create_student(student_model)

        return student_id

    def creating_students(self, student_list: List[CreateStudent]):
        student_model_list = []
        point = self.point_service.get_point_home_by_user_id(student_list[0].responsible_id)
        responsible_data = self.user_service.get_user(student_list[0].responsible_id)

        for student in student_list:
            if(student.id == None):
                student_code = self.generate_student_code(student.name, responsible_data.uuid)
                student_model = StudentModel(name=student.name, year=student.year, code=student_code, point_id=point.id, creation_user=student.responsible_id)
                student_model_list.append(student_model)

        student_id = self.student_repository.create_student_list(student_model_list)

        return student_id
    
    def generate_student_code(self, name: str, responsible_uuid: str):
        initials = "".join([separate_name[0].upper() for separate_name in name.split()])
        
        uuid_simples = responsible_uuid[:6]
        return f"{initials[0]}{uuid_simples}{initials[-1]}"
    
    def validating_association(self, association: StudentAssociation):
        user = self.user_service.get_user(association.responsible_id)

        if(user is None):
            raise ValueError("Usuário não encontrado")
        
        if(user.user_type_id == 2):
            raise ValueError("Usuário não é um responsável")
        
        user_student = self.user_student_service.get_students_by_responsible(association.responsible_id)

        if(len(user_student) > 0):
            student_ids_list = []

            for student in user_student:
                student_id = student.student_id
                student_ids_list.append(student_id)

            if(association.student_id in student_ids_list):
                raise ValueError("Aluno já associado")
            
    def validating_disassociation(self, disassociation: StudentAssociation):
        user = self.user_service.get_user(disassociation.responsible_id)

        if(user is None):
            raise ValueError("Usuário não encontrado")
        
        if(user.user_type_id == 2):
            raise ValueError("Usuário não é um responsável")
        
        student = self.student_repository.get_student(disassociation.student_id)

        if(student.creation_user == disassociation.responsible_id):
            raise ValueError("Não é possível desassociar")

        user_student = self.user_student_service.get_students_by_responsible(disassociation.responsible_id)

        if(len(user_student) > 0):
            student_ids_list = []

            for student in user_student:
                student_id = student.student_id
                student_ids_list.append(student_id)

            if(disassociation.student_id not in student_ids_list):
                raise ValueError("Aluno não associado")

