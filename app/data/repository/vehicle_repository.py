from sqlalchemy.orm import Session
from data.model.vehicle_model import VehicleModel
from data.infrastructure.database import get_db

class VehicleRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_vehicle(self, db_vehicle: VehicleModel):
        try:
            self.db.add(db_vehicle)
            self.db.commit()
            return db_vehicle.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    