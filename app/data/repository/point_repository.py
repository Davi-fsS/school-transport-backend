from sqlalchemy.orm import Session
from data.model.point_model import PointModel
from data.infrastructure.database import get_db

class PointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_point(self, db_point: PointModel):
        try:
            self.db.add(db_point)
            self.db.commit()
            return db_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    