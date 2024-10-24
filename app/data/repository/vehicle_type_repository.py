from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.vehicle_type_model import VehicleTypeModel

class VehicleTypeRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_type(self, type_id: int):
        try:
            return self.db.query(VehicleTypeModel).filter(VehicleTypeModel.id == type_id).first()   
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")