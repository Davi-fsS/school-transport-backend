from typing import List
from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.user_phone_model import UserPhoneModel
from presentation.dto.UpdatePhone import UpdatePhone

class UserPhoneRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_user_phone_list(self, user_id: int):
        try:
            return self.db.query(UserPhoneModel).filter(UserPhoneModel.user_id == user_id, UserPhoneModel.disabled == False).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        
    def get_user_phone_list_by_list(self, user_id_list: List[int]):
        return self.db.query(UserPhoneModel).filter(UserPhoneModel.user_id.in_(user_id_list), UserPhoneModel.disabled == False).all() 

    def create_phone(self, db_user_phone: UserPhoneModel):
        try:
            self.db.add(db_user_phone)
            self.db.commit()
            return db_user_phone.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    