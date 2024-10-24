from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
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
            
            id = db_coordinate.id
            return id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def get_list_coordinates_by_schedule_id(self, schedule_id: int):
            list = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id == schedule_id).all()
            return list
    
    def get_list_coordinates_by_schedule_list(self, schedule_list: List[int]):
        list = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id.in_(schedule_list), CoordinateModel.coordinate_type_id == 1).all()
        return list

    def get_list_lora_coordinates_by_schedule_list(self, schedule_list: List[int]):
        list = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id.in_(schedule_list), CoordinateModel.coordinate_type_id == 2).all()
        return list

    def get_last_coordinate_by_schedule_id(self, schedule_id: int):
        coord = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id == schedule_id).order_by(desc(CoordinateModel.id)).first()
        return coord