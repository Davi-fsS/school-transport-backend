from sqlalchemy.orm import Session
from data.model.user_phone_model import UserPhoneModel
from data.infrastructure.database import get_db
from presentation.dto.UserDto import UserDto

class UserPhoneRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_phone(self, user_id: int, user: UserDto):
        return
    