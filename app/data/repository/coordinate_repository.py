from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from data.infrastructure.database import SessionManager
from data.model.coordinate_model import CoordinateModel

class CoordinateRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def save_coordinates(self, db_coordinate: CoordinateModel):
        try:
            self.db.add(db_coordinate)
            self.db.commit()
            
            id = db_coordinate.id
            self.session_manager.close(self.db)
            return id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def get_list_coordinates_by_schedule_id(self, schedule_id: int):
        try:
            list = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id == schedule_id).all()
            self.session_manager.close(self.db)
            return list
        finally:
            self.session_manager.close(self.db)
    
    def get_list_coordinates_by_schedule_list(self, schedule_list: List[int]):
        try:
            list = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id.in_(schedule_list), CoordinateModel.coordinate_type_id == 1).all()
            self.session_manager.close(self.db)
            return list
        finally:
            self.session_manager.close(self.db)

    def get_list_lora_coordinates_by_schedule_list(self, schedule_list: List[int]):
        try:
            list = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id.in_(schedule_list), CoordinateModel.coordinate_type_id == 2).all()
            self.session_manager.close(self.db)
            return list
        finally:
            self.session_manager.close(self.db)

    def get_last_coordinate_by_schedule_id(self, schedule_id: int):
        try:
            coord = self.db.query(CoordinateModel).filter(CoordinateModel.schedule_id == schedule_id).order_by(desc(CoordinateModel.id)).first()
            self.session_manager.close(self.db)
            return coord
        finally:
            self.session_manager.close(self.db)