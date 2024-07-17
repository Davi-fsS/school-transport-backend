from typing import List
from data.repository.user_student_repository import UserStudentRepository
from data.model.user_student_model import UserStudentModel

class UserStudentService():
    user_student_repository: UserStudentRepository

    def __init__(self):
        self.user_student_repository = UserStudentRepository()

    def create_user_student(self, user_id: int, student_id: int):
        user_student_model = UserStudentModel(user_id=user_id, student_id=student_id, creation_user=2)
        
        return self.user_student_repository.create_user_student(user_student_model)
    
    def create_user_student_list(self, user_id: int, student_id_list: List[int]):
        user_student_model_list = []
        
        for student_id in student_id_list:
            user_student_model = UserStudentModel(user_id=user_id, student_id=student_id, creation_user=2)
            user_student_model_list.append(user_student_model)
        
        return self.user_student_repository.create_user_student_list(user_student_model_list)

    def delete_user_student(self, student_id: int):
        return self.user_student_repository.delete_user_student(student_id=student_id)