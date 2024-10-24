from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.schedule_maps_infos_model import ScheduleMapsInfosModel

class ScheduleMapsInfosRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_schedule_maps_infos_by_schedule_id(self, schedule_id: int):
        return self.db.query(ScheduleMapsInfosModel).filter(ScheduleMapsInfosModel.schedule_id == schedule_id).first()
