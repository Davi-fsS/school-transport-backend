from typing import List
from sqlalchemy.orm import Session
from data.infrastructure.database import get_db
from data.model.parent_notification_model import ParentNotificationModel
from datetime import datetime
from sqlalchemy import func, cast, Date
import pytz

class ParentNotificationRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_notification_list_by_user(self, user_id: int):
        return self.db.query(ParentNotificationModel).filter(ParentNotificationModel.user_id == user_id, ParentNotificationModel.disabled == False).all()
   
    def get_notification_list_by_student_list(self, student_list: List[int]):
        timezone = pytz.timezone('America/Sao_Paulo')
        current_date = datetime.now(timezone).date()

        return self.db.query(ParentNotificationModel).filter(
            ParentNotificationModel.student_id.in_(student_list),
            cast(ParentNotificationModel.inative_day, Date) == current_date,
            ParentNotificationModel.disabled == False
        ).all()

    def get_canceled_notification_list_by_user(self, user_id: int):
        return self.db.query(ParentNotificationModel).filter(ParentNotificationModel.user_id == user_id, ParentNotificationModel.disabled == True).all()
   
    def get_by_id(self, id: int):
        return self.db.query(ParentNotificationModel).filter(ParentNotificationModel.id == id, ParentNotificationModel.disabled == False).first()

    def get_notification_list_after_today_by_user(self, user_id: int):
        return self.db.query(ParentNotificationModel).filter(ParentNotificationModel.user_id == user_id, cast(ParentNotificationModel.inative_day, Date) >= cast(func.now(), Date),ParentNotificationModel.disabled == False).all()

    def get_notification_list_past_by_user(self, user_id: int):
        return self.db.query(ParentNotificationModel).filter(ParentNotificationModel.user_id == user_id, cast(ParentNotificationModel.inative_day, Date) < cast(func.now(), Date),ParentNotificationModel.disabled == False).all()

    def create_notification(self, body: ParentNotificationModel):
        try:
            self.db.add(body)
            self.db.commit()
            return body.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    
    def put_notification_disabled(self, id: int):
        try:
            notification = self.get_by_id(id)

            notification.disabled = True
            notification.change_date = datetime.now()
            notification.change_user = notification.user_id

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")