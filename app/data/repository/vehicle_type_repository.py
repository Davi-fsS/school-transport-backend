from sqlalchemy.orm import Session
from data.model.vehicle_type_model import VehicleTypeModel
from data.infrastructure.database import get_db

class VehicleTypeRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_type(self, type_id: int):
        return self.db.query(VehicleTypeModel).filter(VehicleTypeModel.id == type_id).first()