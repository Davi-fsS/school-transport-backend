from sqlalchemy.orm import Session
from data.model.student_model import StudentModel
from data.infrastructure.database import get_db

class StudentRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_student(self, db_student: StudentModel):
        try:
            self.db.add(db_student)
            self.db.commit()
            return db_student.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    