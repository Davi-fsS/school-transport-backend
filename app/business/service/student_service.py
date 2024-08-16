from typing import List
from data.repository.student_repository import StudentRepository
from business.service.user_service import UserService
from business.service.point_service import PointService
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.StudentAssociation import StudentAssociation
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
    
    def get_student_by_code(self, code: str):
        student = self.student_repository.get_student_by_code(code)

        if(student is None):
            raise ValueError("Aluno não encontrado")
        
        return student

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

        driver = self.user_service.get_user_by_code(student.driver_code)

        self.user_student_service.create_user_student(student_id=student_id, user_id=driver.id)

    def create_student_list(self, student_list: List[CreateStudent]):
        self.validate_create_student_list(student_list=student_list)

        student_id_list = self.creating_students(student_list=student_list)

        self.user_student_service.create_user_student_list(student_id_list=student_id_list, user_id=student_list[0].responsible_id)
    
    def update_student(self, student: UpdateStudent):
        self.validate_update_student(student=student)

        return self.student_repository.update_student(student_update=student)
    
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

