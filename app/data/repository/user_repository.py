from sqlalchemy.orm import Session
from data.model.user_model import UserModel

class UserRepository():
    user: UserModel

    def __init__(self):
        self.user = UserModel()

    def get_user(self, db: Session, id: int):
        return db.query(self.user).filter(self.user.id == id).first()