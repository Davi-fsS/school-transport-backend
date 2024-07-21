from sqlalchemy.orm import Session
from data.model.point_model import PointModel
from data.infrastructure.database import get_db

class PointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_point(self, point_id: int):
        try:
            return self.db.query(PointModel).filter(PointModel.id == point_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def create_point(self, db_point: PointModel):
        try:
            self.db.add(db_point)
            self.db.commit()
            return db_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    