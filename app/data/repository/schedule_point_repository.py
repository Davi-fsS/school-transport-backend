from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, date
from data.infrastructure.database import SessionManager
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from data.model.schedule_point_model import SchedulePointModel
from sqlalchemy import func, cast, Date

class SchedulePointRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_schedule_point_list_by_schedule_id(self, schedule_id: int):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.schedule_id == schedule_id).order_by(SchedulePointModel.order).all()
        finally:
            self.session_manager.close(self.db)

    def get_schedule_point_by_id(self, id: int):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.id == id).first()
        finally:
            self.session_manager.close(self.db)

    def get_last_schedule_point(self, schedule_id : int):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.schedule_id == schedule_id).order_by(desc(SchedulePointModel.order)).first()
        finally:
            self.session_manager.close(self.db)

    def get_current_schedule_point_by_schedule_id(self, schedule_id: int):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.schedule_id == schedule_id, SchedulePointModel.real_date == None).first()
        finally:
            self.session_manager.close(self.db)

    def get_schedule_point_by_point_id(self, schedule_id: int, point_id: int):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.point_id == point_id,SchedulePointModel.schedule_id == schedule_id, SchedulePointModel.real_date == None).first()
        finally:
            self.session_manager.close(self.db)

    def get_schedule_point_by_point_list(self, point_list: List[int]):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.point_id.in_(point_list)).all()
        finally:
            self.session_manager.close(self.db)
    
    def get_schedule_point_by_point_list_date(self, point_list: List[int], date: date):
        try:
            return self.db.query(SchedulePointModel).filter(SchedulePointModel.point_id.in_(point_list), cast(SchedulePointModel.real_date, Date) == date).all()
        finally:
            self.session_manager.close(self.db)

    def put_schedule_point(self, schedule_id: int, point_id: int, user_id: int, has_embarked: bool):
        try:
            sched_point = self.get_schedule_point_by_point_id(schedule_id, point_id)

            sched_point.real_date = datetime.now()
            sched_point.change_user = user_id
            sched_point.has_embarked = has_embarked
            sched_point.change_date = datetime.now()

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.session_manager.close(self.db)