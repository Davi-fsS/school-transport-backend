from sqlalchemy.orm import Session
from data.model.schedule_maps_infos_model import ScheduleMapsInfosModel
from data.infrastructure.database import get_db

class ScheduleMapsInfosRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_schedule_maps_infos_by_schedule_id(self, schedule_id: int):
        return self.db.query(ScheduleMapsInfosModel).filter(ScheduleMapsInfosModel.schedule_id == schedule_id).first()