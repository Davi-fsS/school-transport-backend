from sqlalchemy.orm import Session
from data.model.user_type_model import UserTypeModel
from data.infrastructure.database import get_db

class UserTypeRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_type(self, type_id: int):
        return self.db.query(UserTypeModel).filter(UserTypeModel.id == type_id).first()