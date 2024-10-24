from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.student_model import StudentModel
from data.model.user_student_model import UserStudentModel
from data.model.user_phone_model import UserPhoneModel
from data.model.user_point_model import UserPointModel
from data.model.user_model import UserModel
from presentation.dto.UpdateUser import UpdateUser
from typing import List
from datetime import datetime
from sqlalchemy import inspect

class UserRepository():
    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_user(self, user_id: int):
        try:
            return self.db.query(UserModel).filter(UserModel.id == user_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")   

    def get_user_by_code(self, code: str):
        try:
            return self.db.query(UserModel).filter(UserModel.code == code).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")   

    def get_user_by_list(self, user_id_list : List[int]):
        try:
            return self.db.query(UserModel).filter(UserModel.id.in_(user_id_list)).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        
    def get_responsibles_by_list(self, user_id_list : List[int]):
        return self.db.query(UserModel).filter(UserModel.id.in_(user_id_list), UserModel.user_type_id != 2).all()

    def get_all_drivers(self):
        try:
            return self.db.query(UserModel).filter(UserModel.user_type_id == 2).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def get_user_by_email(self, email: str):
        try:
            return self.db.query(UserModel).filter(UserModel.email == email).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")    
            
    def get_user_by_cnh(self, cnh: str):
        try:
            return self.db.query(UserModel).filter(UserModel.cnh == cnh).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")    

    def get_user_by_cpf(self, cpf: str):
        try:
            return self.db.query(UserModel).filter(UserModel.cpf == cpf).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def get_user_by_rg(self, rg: str):
        try:
            return self.db.query(UserModel).filter(UserModel.rg == rg).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")       

    def create_user(self, db_user: UserModel):
        try:
            self.db.add(db_user)
            self.db.commit()
            return db_user.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    def update_user_uuid(self, id: int, uuid: str):
        try:
            user = self.get_user(id)
            if user is None:
                raise ValueError("Usuário não encontrado")

            user.uuid = uuid
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")        

    def update_user(self, user_update: UpdateUser):
        try:
            user = self.get_user(user_update.id)

            user.name = user_update.name
            user.email = user_update.email
            user.cpf = user_update.cpf
            user.cnh = user_update.cnh
            user.rg = user_update.rg

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    def update_user_code(self, user_update_id: int, code: str):
        try:
            user = self.get_user(user_update_id)

            user.code = code

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    def delete_user(self, user: UserModel, user_point_list: List[UserPointModel], user_phone_list: List[UserPhoneModel], 
                user_students: List[UserStudentModel], others_user_students: List[UserStudentModel], 
                students_created_by_user: List[StudentModel], students_associated_by_user: List[StudentModel]):
        try:
            today = datetime.now()

            user = self.db.merge(user)

            user_point_list = [self.db.merge(user_point) for user_point in user_point_list]
            user_phone_list = [self.db.merge(user_phone) for user_phone in user_phone_list]
            user_students = [self.db.merge(user_student) for user_student in user_students]
            others_user_students = [self.db.merge(others_user_student) for others_user_student in others_user_students]
            students_created_by_user = [self.db.merge(student_created_by_user) for student_created_by_user in students_created_by_user]
            students_associated_by_user = [self.db.merge(student_associated_by_user) for student_associated_by_user in students_associated_by_user]

            user.disabled = True
            user.change_date = today
            user.change_user = user.id

            for user_point in user_point_list:
                user_point.disabled = True
                user_point.change_date = today
                user_point.change_user = user.id

            for user_phone in user_phone_list:
                user_phone.disabled = True
                user_phone.change_date = today
                user_phone.change_user = user.id

            for user_student in user_students:
                user_student.disabled = True
                user_student.change_date = today
                user_student.change_user = user.id

            for others_user_student in others_user_students:
                others_user_student.disabled = True
                others_user_student.change_date = today
                others_user_student.change_user = user.id

            for student_created_by_user in students_created_by_user:
                student_created_by_user.disabled = True
                student_created_by_user.change_date = today
                student_created_by_user.change_user = user.id
            
            for student_associated_by_user in students_associated_by_user:
                student_associated_by_user.change_date = today
                student_associated_by_user.change_user = user.id

            self.db.flush()

            self.db.commit()

            self.db.refresh(user)
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Erro ao salvar no sistema: {e}")
