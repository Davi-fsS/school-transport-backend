from data.repository.user_student_repository import UserStudentRepository
from data.model.user_student_model import UserStudentModel

class UserStudentService():
    user_student_repository: UserStudentRepository

    def __init__(self):
        self.user_student_repository = UserStudentRepository()

    def create_user_student(self, user_id: int, student_id: int):
        user_student_model = UserStudentModel(user_id=user_id, student_id=student_id, creation_user=2)
        
        return self.user_student_repository.create_user_student(user_student_model)
