from sqlalchemy.orm import Session
from data.model.schedule_point_model import SchedulePointModel
from data.infrastructure.database import get_db

class SchedulePointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_schedule_point_list_by_schedule_id(self, schedule_id: int):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.schedule_id == schedule_id).order_by(SchedulePointModel.order).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")