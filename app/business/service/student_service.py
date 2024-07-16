from data.repository.student_repository import StudentRepository
from presentation.dto.CreateStudent import CreateStudent
from data.model.student_model import StudentModel

class StudentService():
    student_repository: StudentRepository

    def __init__(self):
        self.student_repository = StudentRepository()

    def create_student(self, student: CreateStudent):
        student = StudentModel(name=student.name, age=student.age, creation_user=2)

        return self.student_repository.create_student(student)