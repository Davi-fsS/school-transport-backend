from typing import List
from sqlalchemy.orm import Session
from data.model.user_student_model import UserStudentModel
from data.infrastructure.database import get_db

class UserStudentRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_user_student(self, db_user_student: UserStudentModel):
        try:
            self.db.add(db_user_student)
            self.db.commit()
            return db_user_student.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def create_user_student_list(self, db_user_student_list: List[UserStudentModel]):
        created_ids = []
        try:
            for db_user_student in db_user_student_list:
                self.db.add(db_user_student)
                self.db.commit()
                created_ids.append(db_user_student.id)

            return created_ids
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    