from sqlalchemy.orm import Session
from data.infrastructure.database import get_db
from data.model.coordinate_model import CoordinateModel

class CoordinateRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def save_coordinates(self, db_coordinate: CoordinateModel):
        try:
            self.db.add(db_coordinate)
            self.db.commit()
            return db_coordinate.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        