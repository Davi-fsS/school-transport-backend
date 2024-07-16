from sqlalchemy.orm import Session
from data.model.user_point_model import UserPointModel
from data.infrastructure.database import get_db

class UserPointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_user_point(self, db_user_point: UserPointModel):
        try:
            self.db.add(db_user_point)
            self.db.commit()
            return db_user_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    