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
        return self.db.query(StudentModel).filter(StudentModel.id == student_id).first()

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
            if student is None:
                    raise ValueError("Usuário não encontrado")

            student.name = student_update.name
            student.year = student_update.year
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    