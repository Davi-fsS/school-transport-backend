from sqlalchemy.orm import Session
from data.model.user_model import UserModel
from data.infrastructure.database import get_db
from presentation.dto.UserDto import UserDto

class UserRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_user(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_user_by_cnh(self, cnh: str):
        return self.db.query(UserModel).filter(UserModel.cnh == cnh).first()
    
    def get_user_by_cpf(self, cpf: str):
        return self.db.query(UserModel).filter(UserModel.cpf == cpf).first()
    
    def get_user_by_rg(self, rg: str):
        return self.db.query(UserModel).filter(UserModel.rg == rg).first()

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