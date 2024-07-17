from typing import List
from business.service.student_service import StudentService
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.UpdateStudent import UpdateStudent

class StudentController():
    student_service: StudentService

    def __init__(self):
        self.student_service = StudentService()
    
    def create_student_list(self, student_list: List[CreateStudent]):
        return self.student_service.create_student_list(student_list=student_list)
    
    def update_student(self, student: UpdateStudent):
        return self.student_service.update_student(student=student)
