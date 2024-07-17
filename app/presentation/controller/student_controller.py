from typing import List
from business.service.student_service import StudentService
from presentation.dto.CreateStudent import CreateStudent

class StudentController():
    student_service: StudentService

    def __init__(self):
        self.student_service = StudentService()
    
    def create_student_list(self, student_list: List[CreateStudent]):
        return self.student_service.create_student_list(student_list=student_list)
