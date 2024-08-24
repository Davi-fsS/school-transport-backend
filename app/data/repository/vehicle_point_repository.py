from sqlalchemy.orm import Session
from data.model.vehicle_point_model import VehiclePointModel
from data.infrastructure.database import get_db

class VehiclePointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_vehicle_point_association(self, vehicle_id: int, point_id: int):
        try:
            return self.db.query(VehiclePointModel).filter(VehiclePointModel.point_id == point_id,
                                                            VehiclePointModel.vehicle_id == vehicle_id,
                                                            VehiclePointModel.disabled == False).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")