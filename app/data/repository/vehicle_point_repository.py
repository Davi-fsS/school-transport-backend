from typing import List
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
        
    def get_vehicle_point_association_by_vehicle_list(self, vehicle_list: List[int]):
        return self.db.query(VehiclePointModel).filter(VehiclePointModel.vehicle_id.in_(vehicle_list), VehiclePointModel.disabled == False).all()
    
    def get_vehicle_point_association_by_point_list(self, point_list: List[int]):
        return self.db.query(VehiclePointModel).filter(VehiclePointModel.point_id.in_(point_list), VehiclePointModel.disabled == False).all()