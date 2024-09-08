from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from presentation.dto.Point import Point
from data.model.schedule_point_model import SchedulePointModel
from data.model.schedule_user_model import ScheduleUserModel
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
        return self.db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id).first()
    
    def create_schedule_destiny_school(self, schedule: CreateSchedule, driver: UserModel, vehicle: VehicleModel, school: PointModel):
        try:
            creation_date = datetime.now()

            schedule = ScheduleModel(name=schedule.schedule_name, initial_date=creation_date,
                                    end_date = schedule.end_date, description=f"Viagem de ida para {school.name} - {creation_date.date()}",
                                    schedule_type_id=1, creation_user=driver.id)
            
            self.db.add(schedule)
            self.db.flush()

            schedule_vehicle = ScheduleVehicleModel(schedule_id=schedule.id, vehicle_id=vehicle.id, creation_user= driver.id)

            self.db.add(schedule_vehicle)

            schedule_user = ScheduleUserModel(schedule_id=schedule.id, user_id=driver.id, creation_user=driver.id)

            self.db.add(schedule_user)

            self.db.commit()

            return schedule.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")
        
    def create_schedule_origin_school(self, schedule: CreateSchedule, driver: UserModel, vehicle: VehicleModel, school: PointModel):
        try:
            creation_date = datetime.now()

            schedule = ScheduleModel(name=schedule.schedule_name, initial_date=creation_date,
                                    end_date = schedule.end_date, description=f"Viagem de volta de {school.name} - {creation_date.date()}",
                                    schedule_type_id=2, creation_user=driver.id)
            
            self.db.add(schedule)
            self.db.flush()

            schedule_vehicle = ScheduleVehicleModel(schedule_id=schedule.id, vehicle_id=vehicle.id, creation_user= driver.id)

            self.db.add(schedule_vehicle)

            schedule_user = ScheduleUserModel(schedule_id=schedule.id, user_id=driver.id, creation_user=driver.id)

            self.db.add(schedule_user)
            
            self.db.commit()

            return schedule.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")

    def put_schedule_start(self, schedule_id: int, points: List[int], school: Point, user_id: int):
        try:
            schedule = self.get_schedule_by_id(schedule_id)

            if(schedule is None):
                raise ValueError("Viagem não encontrada")
            
            schedule.real_initial_date = datetime.now()

            if(schedule.schedule_type_id == 1):
                for index, point in enumerate(points):
                    print(index)
                    schedule_point = SchedulePointModel(schedule_id=schedule.id, order=index + 1,point_id=point, creation_user=user_id)
                    self.db.add(schedule_point)

                schedule_point_school = SchedulePointModel(schedule_id=schedule.id, order=len(points) + 1, point_id=school.id, description=f"Destino: Escola {school.name}" ,creation_user=user_id)
                self.db.add(schedule_point_school)
            else:
                schedule_point_school = SchedulePointModel(schedule_id=schedule.id, order=1, point_id=school.id, description=f"Origem: Escola {school.name}" ,creation_user=user_id)
                self.db.add(schedule_point_school)

                for index, point in enumerate(points, start=1):
                    schedule_point = SchedulePointModel(schedule_id=schedule.id, order=index + 1,point_id=point, creation_user=user_id)
                    self.db.add(schedule_point)

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")
