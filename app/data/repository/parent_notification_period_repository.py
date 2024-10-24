from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.parent_notification_period_model import ParentNotificationPeriodModel

class ParentNotificationPeriodRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_all(self):
        try:
            return self.db.query(ParentNotificationPeriodModel).all()
        finally:
            self.session_manager.close(self.db)