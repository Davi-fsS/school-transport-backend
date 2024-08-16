from sqlalchemy.orm import Session
from data.model.user_model import UserModel
from data.infrastructure.database import get_db
from presentation.dto.UpdateUser import UpdateUser
from typing import List

class UserRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

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
        
    def delete_user(self, user_id: int):
        try:
            user = self.get_user(user_id)
            self.db.delete(user)
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")