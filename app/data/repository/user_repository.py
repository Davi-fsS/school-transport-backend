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
    
    def create_user(self, user: UserDto):
        try:
            db_user = UserModel(**user.model_dump())
            self.db.add(db_user)
            self.db.commit()
            return user.model_dump()
        except:
            self.db.rollback()
            raise ValueError
