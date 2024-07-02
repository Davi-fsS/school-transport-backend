from business.service.user_service import UserService
from sqlalchemy.orm import Session

class UserController():
    user_service: UserService

    def __init__(self):
        self.user_service = UserService()
    
    def read_user(self, db: Session, id: int):
        return self.user_service.get_user(db, id)