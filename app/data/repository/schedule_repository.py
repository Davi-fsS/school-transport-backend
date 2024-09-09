from datetime import datetime
from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import Session
from data.model.schedule_maps_infos_model import ScheduleMapsInfosModel
from presentation.dto.StartSchedule import StartSchedule
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
    
    def get_last_schedule_point(self, schedule_id : int):
        return self.db.query(SchedulePointModel).filter(SchedulePointModel.schedule_id == schedule_id).order_by(desc(SchedulePointModel.order)).first()
    
    def get_schedule_not_started(self, schedule_id: int):
        return self.db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id, ScheduleModel.real_initial_date == None, 
                                                   ScheduleModel.real_end_date == None).first()

    def get_schedule_in_progress(self, schedule_id: int):
        return self.db.query(ScheduleModel).filter(ScheduleModel.id == schedule_id, ScheduleModel.real_initial_date != None, 
                                                   ScheduleModel.real_end_date == None).first()

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

    def put_schedule_start(self, start: StartSchedule):
        try:
            schedule = self.get_schedule_not_started(start.schedule_id)

            if(schedule is None):
                raise ValueError("Viagem não encontrada")
            
            schedule.real_initial_date = datetime.now()

            if(schedule.schedule_type_id == 1):
                for index, point in enumerate(start.points):
                    schedule_point = SchedulePointModel(schedule_id=schedule.id, order=index + 1,point_id=point, creation_user=start.user_id)
                    self.db.add(schedule_point)

                schedule_point_school = SchedulePointModel(schedule_id=schedule.id, order=len(start.points) + 1, point_id=start.school.id, description=f"Destino: Escola {start.school.name}" ,creation_user=start.user_id)
                self.db.add(schedule_point_school)
            else:
                schedule_point_school = SchedulePointModel(schedule_id=schedule.id, order=1, point_id=start.school.id, description=f"Origem: Escola {start.school.name}" ,creation_user=start.user_id)
                self.db.add(schedule_point_school)

                for index, point in enumerate(start.points, start=1):
                    schedule_point = SchedulePointModel(schedule_id=schedule.id, order=index + 1,point_id=point, creation_user=start.user_id)
                    self.db.add(schedule_point)

            schedule_map_infos = ScheduleMapsInfosModel(schedule_id=schedule.id, encoded_points=start.encoded_points, legs_info=start.legs_info,
                                                        eta=start.eta, creation_user = start.user_id)

            self.db.add(schedule_map_infos)

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")
    
    def put_schedule_end(self, schedule: ScheduleModel, user_id: int):
        try:
            today_datetime = datetime.now()

            schedule.real_end_date = today_datetime
            schedule.change_user = user_id
            schedule.change_date = today_datetime

            last_point = self.get_last_schedule_point(schedule.id)

            last_point.real_initial_date = today_datetime
            last_point.real_end_date = today_datetime
            last_point.change_user = user_id
            last_point.change_date = today_datetime
                    
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")