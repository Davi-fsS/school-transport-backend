from data.repository.user_repository import UserRepository
from sqlalchemy.orm import Session

class UserService():
    user_repository : UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, db: Session, id:int):
        return self.user_repository.get_user(db, id)