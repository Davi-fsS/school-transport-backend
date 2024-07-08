from sqlalchemy.orm import Session
from data.model.user_phone_model import UserPhoneModel
from data.infrastructure.database import get_db
from presentation.dto.CreatePhone import CreatePhone

class UserPhoneRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_phone(self, db_user_phone: UserPhoneModel):
        try:
            self.db.add(db_user_phone)
            self.db.commit()
            return db_user_phone.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    