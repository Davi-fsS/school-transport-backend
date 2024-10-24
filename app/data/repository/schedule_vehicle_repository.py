from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.schedule_vehicle_model import ScheduleVehicleModel

class ScheduleVehicleRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_schedule_vehicle_by_schedule_id(self, schedule_id: int):
        try:
            return self.db.query(ScheduleVehicleModel).filter(ScheduleVehicleModel.schedule_id == schedule_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)