from sqlalchemy.orm import Session
from data.model.user_student_model import UserStudentModel
from data.infrastructure.database import get_db

class StudentRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_user_point(self, db_user_student: UserStudentModel):
        try:
            self.db.add(db_user_student)
            self.db.commit()
            return db_user_student.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    