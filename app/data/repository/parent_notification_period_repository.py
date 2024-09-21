from sqlalchemy.orm import Session
from data.model.parent_notification_period_model import ParentNotificationPeriodModel
from data.infrastructure.database import get_db

class ParentNotificationPeriodRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_all(self):
        return self.db.query(ParentNotificationPeriodModel).all()