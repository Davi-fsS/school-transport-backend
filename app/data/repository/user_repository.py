from sqlalchemy.orm import Session
from data.model.user_model import UserModel
from data.infrastructure.database import get_db

class UserRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_user(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
