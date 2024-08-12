from typing import List
from sqlalchemy.orm import Session
from data.model.student_model import StudentModel
from presentation.dto.UpdateStudent import UpdateStudent
from data.infrastructure.database import get_db

class StudentRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_student(self, student_id: int):
        try:
            student = self.db.query(StudentModel).filter(StudentModel.id == student_id).first()

            if student is None:
                raise ValueError("Aluno não encontrado")

            return student
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        
    def get_student_by_code(self, student_code: str):
        try:
            student = self.db.query(StudentModel).filter(StudentModel.code == student_code).first()

            return student
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        
    def get_students_by_student_list(self, student_id_list: List[int]):
        try:
            students = self.db.query(StudentModel).filter(StudentModel.id.in_(student_id_list)).all()
            return students
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def create_student_list(self, db_student_list: List[StudentModel]):
        created_ids = []
        try:
            for db_student in db_student_list:
                self.db.add(db_student)
                self.db.commit()
                created_ids.append(db_student.id)

            return created_ids
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def update_student(self, student_update: UpdateStudent):
        try:
            student = self.get_student(student_update.id)
            student.name = student_update.name
            student.year = student_update.year
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def delete_student(self, student_id: int):
        try:
            student = self.get_student(student_id)
            self.db.delete(student)
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    