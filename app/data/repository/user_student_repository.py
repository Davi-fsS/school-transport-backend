from typing import List
from sqlalchemy.orm import Session
from data.model.user_student_model import UserStudentModel
from data.infrastructure.database import get_db

class UserStudentRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_user_student(self, student_id: int, responsible_id: int):
        try:
            user_student = self.db.query(UserStudentModel).filter(UserStudentModel.student_id == student_id, UserStudentModel.user_id == responsible_id, UserStudentModel.disabled == False).first()

            if user_student is None:
                raise ValueError("Associação entre aluno e responsável não encontrada")

            return user_student 
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema") 

    def get_user_student_by_student_id(self, student_id: int):
        try:
            user_student = self.db.query(UserStudentModel).filter(UserStudentModel.student_id == student_id, UserStudentModel.disabled == False).first()

            if user_student is None:
                raise ValueError("Associação entre aluno e responsável não encontrada")

            return user_student 
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")    
        
    def get_all_user_student_by_student_id(self, student_id: int):
        try:
            user_student = self.db.query(UserStudentModel).filter(UserStudentModel.student_id == student_id, UserStudentModel.disabled == False).all()

            if user_student is None:
                raise ValueError("Associação entre aluno e responsável não encontrada")

            return user_student 
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def get_students_by_responsible(self, responsible_id: int):
        try:
            user_student_list = self.db.query(UserStudentModel).filter(UserStudentModel.user_id == responsible_id, UserStudentModel.disabled == False).all()

            return user_student_list 
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        
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
        
    def delete_user_student_by_student_id(self, student_id: int):
        try:
            user_student = self.get_user_student_by_student_id(student_id)
            user_student.disabled = True
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def delete_all_user_student_by_student_id(self, student_id: int):
        try:
            user_student_list = self.get_all_user_student_by_student_id(student_id)

            for user_student in user_student_list:
                user_student.disabled = True
                self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def delete_user_student(self, student_id: int, responsible_id: int):
        try:
            user_student = self.get_user_student(student_id, responsible_id)
            user_student.disabled = True
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")