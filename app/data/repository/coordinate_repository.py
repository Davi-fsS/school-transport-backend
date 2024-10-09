from typing import List
from sqlalchemy.orm import Session
from data.infrastructure.database import get_db
from sqlalchemy import desc
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
        
    def get_list_coordinates_by_schedule_id(self, schedule_id: int):
        return self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id == schedule_id).all()
    
    def get_list_coordinates_by_schedule_list(self, schedule_list: List[int]):
        return self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id.in_(schedule_list)).all()
    
    def get_last_coordinate_by_schedule_id(self, schedule_id: int):
        return self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id == schedule_id).order_by(desc(CoordinateModel.id)).first()