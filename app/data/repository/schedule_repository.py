from datetime import date, datetime
from sqlalchemy import Date, desc
from typing import List
from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
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
from sqlalchemy import func, cast, Date

class ScheduleRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

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

    def get_schedule_list_in_progress_by_list(self, schedule_id_list: List[int]):
        return self.db.query(ScheduleModel).filter(ScheduleModel.id.in_(schedule_id_list), ScheduleModel.real_initial_date != None, 
                                                   ScheduleModel.real_end_date == None).all()

    def get_schedule_list_by_list_and_date(self, schedule_id_list: List[int], date: date):
        return self.db.query(ScheduleModel).filter(ScheduleModel.id.in_(schedule_id_list), 
                                                   cast(ScheduleModel.initial_date, Date) == date).all()

    def get_schedule_list_by_list(self, schedule_id_list: List[int]):
        return self.db.query(ScheduleModel).filter(ScheduleModel.id.in_(schedule_id_list)).all()

    def create_schedule(self, schedule: CreateSchedule, driver: UserModel, vehicle: VehicleModel, school: PointModel):
        try:
            creation_date = datetime.now()

            if(schedule.schedule_type != 1 and schedule.schedule_type != 2):
                raise ValueError("Tipo de viagem inválida")

            schedule_name = f"Ida para {school.name}"
            schedule_description = f"Viagem de ida para {school.name} - {creation_date.date()}"

            if(schedule.schedule_type == 2):
                schedule_name = f"Volta de {school.name}"
                schedule_description = f"Viagem de volta de {school.name} - {creation_date.date()}"

            schedule = ScheduleModel(name=schedule_name, initial_date=creation_date, description=schedule_description,
                                    schedule_type_id=schedule.schedule_type, creation_user=driver.id)
            
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

    def put_schedule_start(self, start: StartSchedule, school: PointModel, destiny: PointModel | None):
        try:
            schedule = self.get_schedule_not_started(start.schedule_id)
            
            schedule.end_date = start.end_date
            schedule.real_initial_date = datetime.now()

            if(schedule.schedule_type_id == 1):
                for index, point in enumerate(start.points):
                    schedule_point = SchedulePointModel(schedule_id=schedule.id, order=index + 1,point_id=point, creation_user=start.user_id)
                    self.db.add(schedule_point)

                schedule_point_school = SchedulePointModel(schedule_id=schedule.id, order=len(start.points) + 1, point_id=school.id, 
                                                           description=f"Destino: Escola {school.name}" , creation_user=start.user_id, planned_date=start.end_date)
                self.db.add(schedule_point_school)
            elif(schedule.schedule_type_id == 2):
                schedule_point_school = SchedulePointModel(planned_date=datetime.now(), real_date=datetime.now(), schedule_id=schedule.id, order=1, point_id=school.id, 
                                                        description=f"Origem: Escola {school.name}" ,creation_user=start.user_id)
                self.db.add(schedule_point_school)

                for index, point in enumerate(start.points, start=1):                
                    schedule_point = SchedulePointModel(schedule_id=schedule.id, order=index + 1,point_id=point, creation_user=start.user_id)
                    self.db.add(schedule_point)

                schedule_point_destiny = SchedulePointModel(planned_date=start.end_date, schedule_id=schedule.id, order=len(start.points) + 2, point_id=start.destiny_id,creation_user=start.user_id)
                
                destiny_description = f"Destino: {destiny.name}"

                if(destiny.point_type_id == 2):
                    destiny_description = f"Destino: Escola {destiny.name}"

                schedule_point_destiny.description = destiny_description
                
                self.db.add(schedule_point_destiny)

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

            last_point.real_date = today_datetime
            last_point.change_user = user_id
            last_point.change_date = today_datetime
                    
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer o registro no sistema")