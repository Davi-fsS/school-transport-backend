from sqlalchemy.orm import Session
from data.model.schedule_model import ScheduleModel
from data.infrastructure.database import get_db

class ScheduleRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_schedule_by_id(self, schedule_id : int):
        try:
            schedule = self.db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id).first()

            return schedule
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()