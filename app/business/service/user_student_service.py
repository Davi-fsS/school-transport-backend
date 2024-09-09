from typing import List
from data.repository.user_phone_repository import UserPhoneRepository
from data.repository.user_repository import UserRepository
from presentation.dto.User import User
from data.repository.user_student_repository import UserStudentRepository
from data.model.user_student_model import UserStudentModel

class UserStudentService():
    user_student_repository: UserStudentRepository
    user_repository: UserRepository
    user_phone_repository: UserPhoneRepository

    def __init__(self):
        self.user_student_repository = UserStudentRepository()
        self.user_repository = UserRepository()
        self.user_phone_repository = UserPhoneRepository()

    def get_students_by_responsible(self, responsible_id: int):
        return self.user_student_repository.get_students_by_responsible(responsible_id=responsible_id)
    
    def get_responsibles_by_student_list(self, student_list: List[int]):
        responsible_list: List[User] = []

        user_student_list = self.get_user_students_by_student_list(student_list)

        user_id_list = []

        for user_student in user_student_list:
            user_id_list.append(user_student.user_id)

        responsibles = self.user_repository.get_responsibles_by_list(user_id_list)

        phones = self.user_phone_repository.get_user_phone_list_by_list(user_id_list)

        for responsible in responsibles:
            phone = list(filter(lambda phone: phone.user_id == responsible.id, phones))

            responsible_list.append(User(id=responsible.id, uuid=responsible.uuid, name=responsible.name, email=responsible.email, cpf=responsible.cpf,
                                         cnh=responsible.cnh, rg=responsible.rg, user_type_id=responsible.user_type_id,
                                         code=responsible.code, phones=phone))

        return responsible_list

    
    def get_user_students_by_student_list(self, student_list: List[int]):
        return self.user_student_repository.get_user_students_by_student_list(student_list)
    
    def get_user_students_by_student_id(self, student_id: int):
        return self.user_student_repository.get_all_user_student_by_student_id(student_id)
    
    def get_responsibles_by_student_id(self, student_id: int):
        user_students = self.user_student_repository.get_all_user_student_by_student_id(student_id)

        print("quantidade de associacoes de user x student:", len(user_students))

        user_id_list = []
        for user_student in user_students:
            user_id_list.append(user_student.user_id)

        print("quantidade de associacoes de user x student ID:", len(user_id_list))

        return self.user_repository.get_responsibles_by_list(user_id_list)

    def create_user_student(self, user_id: int, student_id: int):
        user_student_model = UserStudentModel(user_id=user_id, student_id=student_id, creation_user=2)
        
        return self.user_student_repository.create_user_student(user_student_model)
    
    def create_user_student_list(self, user_id: int, student_id_list: List[int]):
        user_student_model_list = []
        
        for student_id in student_id_list:
            user_student_model = UserStudentModel(user_id=user_id, student_id=student_id, creation_user=2)
            user_student_model_list.append(user_student_model)
        
        return self.user_student_repository.create_user_student_list(user_student_model_list)

    def delete_user_student_by_student_id(self, student_id: int):
        return self.user_student_repository.delete_all_user_student_by_student_id(student_id=student_id)
    
    def delete_user_student(self, student_id: int, responsible_id: int):
        return self.user_student_repository.delete_user_student(student_id=student_id, responsible_id=responsible_id)