from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.schedule_user_model import ScheduleUserModel

class ScheduleUserRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_schedule_user_by_schedule_id(self, schedule_id: int):
        return self.db.query(ScheduleUserModel).filter(ScheduleUserModel.schedule_id == schedule_id).first()

    def get_schedule_user_list_by_user_id(self, user_id: int):
        return self.db.query(ScheduleUserModel).filter(ScheduleUserModel.user_id == user_id).all()