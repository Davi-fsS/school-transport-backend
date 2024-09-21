from sqlalchemy.orm import Session
from data.infrastructure.database import get_db
from data.model.parent_notification_model import ParentNotificationModel

class ParentNotificationRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_notification_list_by_user(self, user_id: int):
        return self.db.query(ParentNotificationModel).filter(ParentNotificationModel.user_id == user_id, ParentNotificationModel.disabled == False).all()

    def create_notification(self, body: ParentNotificationModel):
        try:
            self.db.add(body)
            self.db.commit()
            return body.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")