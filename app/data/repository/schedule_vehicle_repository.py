from sqlalchemy.orm import Session
from data.model.schedule_vehicle_model import ScheduleVehicleModel
from data.infrastructure.database import get_db

class ScheduleVehicleRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_schedule_vehicle_by_schedule_id(self, schedule_id: int):
        try:
            return self.db.query(ScheduleVehicleModel).filter(ScheduleVehicleModel.schedule_id == schedule_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")