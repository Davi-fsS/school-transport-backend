from sqlalchemy.orm import Session
from datetime import datetime
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from data.model.schedule_point_model import SchedulePointModel
from data.infrastructure.database import get_db

class SchedulePointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_schedule_point_list_by_schedule_id(self, schedule_id: int):
        return self.db.query(SchedulePointModel).filter(SchedulePointModel.schedule_id == schedule_id).order_by(SchedulePointModel.order).all()
       
    def get_schedule_point_by_id(self, id: int):
        return self.db.query(SchedulePointModel).filter(SchedulePointModel.id == id).first()
    
    def put_schedule_point(self, id: int, user_id: int):
        try:
            sched_point = self.get_schedule_point_by_id(id)

            sched_point.real_date = datetime.now()
            sched_point.change_user = user_id
            sched_point.change_date = datetime.now()

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")