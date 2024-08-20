from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.data.model.schedule_point_model import SchedulePointModel
from app.data.model.schedule_user_model import ScheduleUserModel
from data.model.point_model import PointModel
from data.model.schedule_vehicle_model import ScheduleVehicleModel
from data.model.user_model import UserModel
from data.model.vehicle_model import VehicleModel
from presentation.dto.CreateSchedule import CreateSchedule
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
        
    def create_schedule_destiny_school(self, schedule: CreateSchedule, driver: UserModel, vehicle: VehicleModel, points: List[PointModel], school: PointModel):
        try:
            creation_date = datetime.now()

            schedule = ScheduleModel(name=schedule.schedule_name, initial_date=creation_date,
                                    end_date = schedule.end_date, real_initial_date = creation_date,
                                    description=f"Viagem de ida para {school.name} - {creation_date.date()}",
                                    schedule_type_id=1, creation_user=driver.id)
            
            self.db.add(schedule)

            schedule_vehicle = ScheduleVehicleModel(schedule_id=schedule.id, vehicle_id=vehicle.id, creation_user= driver.id)

            self.db.add(schedule_vehicle)

            schedule_user = ScheduleUserModel(schedule_id=schedule.id, user_id=driver.id, creation_user=driver.id)

            self.db.add(schedule_user)

            for point in points:
                schedule_point = SchedulePointModel(schedule_id=schedule.id, point_id=point.id, creation_user=driver.id)
                self.db.add(schedule_point)

            schedule_point_school = SchedulePointModel(schedule_id=schedule.id, point_id=school.id, description=f"Destino: Escola {school.name}" ,creation_user=driver.id)

            self.db(schedule_point_school)

            self.db.commit()
            return schedule.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")
        
    def create_schedule_origin_school(self, schedule: CreateSchedule, driver: UserModel, vehicle: VehicleModel, points: List[PointModel], school: PointModel):
        try:
            creation_date = datetime.now()

            schedule = ScheduleModel(name=schedule.schedule_name, initial_date=creation_date,
                                    end_date = schedule.end_date, real_initial_date = creation_date,
                                    description=f"Viagem de volta de {school.name} - {creation_date.date()}",
                                    schedule_type_id=1, creation_user=driver.id)
            
            self.db.add(schedule)

            schedule_vehicle = ScheduleVehicleModel(schedule_id=schedule.id, vehicle_id=vehicle.id, creation_user= driver.id)

            self.db.add(schedule_vehicle)

            schedule_user = ScheduleUserModel(schedule_id=schedule.id, user_id=driver.id, creation_user=driver.id)

            self.db.add(schedule_user)

            schedule_point_school = SchedulePointModel(schedule_id=schedule.id, point_id=school.id, description=f"Origem: Escola {school.name}" ,creation_user=driver.id)

            self.db(schedule_point_school)

            for point in points:
                schedule_point = SchedulePointModel(schedule_id=schedule.id, point_id=point.id,creation_user=driver.id, initial_date=creation_date)
                self.db.add(schedule_point)
            
            self.db.commit()
            return schedule.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")

