from typing import List
from business.service.student_service import StudentService
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.UpdateStudent import UpdateStudent
from presentation.dto.StudentAssociation import StudentAssociation

class StudentController():
    student_service: StudentService

    def __init__(self):
        self.student_service = StudentService()
    
    def get_students_by_responsible(self, responsible_id: int):
        return self.student_service.get_students_by_responsible(responsible_id=responsible_id)

    def get_student_by_code(self, code: str):
        return self.student_service.get_student_by_code(code)

    def get_student_details(self, student_id: int):
        return self.student_service.get_student_details(student_id)

    def create_association_student_responsible(self, association: StudentAssociation):
        return self.student_service.create_association_student_responsible(association)
    
    def disassociation_student_responsible(self, disassociation: StudentAssociation):
        return self.student_service.disassociation_student_responsible(disassociation)

    def create_student(self, student: CreateStudent):
        return self.student_service.create_student(student)

    def create_student_list(self, student_list: List[CreateStudent]):
        return self.student_service.create_student_list(student_list=student_list)
    
    def update_student(self, student: UpdateStudent):
        return self.student_service.update_student(student=student)
    
    def update_student_address(self, student_id: int, user_id: int):
        return self.student_service.update_student_address(student_id, user_id)
   
    def delete_student(self, student_id: int):
        return self.student_service.delete_student(student_id=student_id)
