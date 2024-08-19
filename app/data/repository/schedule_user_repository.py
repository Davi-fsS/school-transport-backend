from sqlalchemy.orm import Session
from data.model.schedule_user_model import ScheduleUserModel
from data.infrastructure.database import get_db

class ScheduleUserRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_schedule_user_by_schedule_id(self, schedule_id: int):
        try:
            return self.db.query(ScheduleUserModel).filter(ScheduleUserModel.schedule_id == schedule_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()