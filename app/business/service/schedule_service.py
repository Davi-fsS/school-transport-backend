from datetime import datetime
from data.model.schedule_vehicle_model import ScheduleVehicleModel
from data.model.schedule_model import ScheduleModel
from business.service.point_service import PointService
from data.repository.point_repository import PointRepository
from business.service.vehicle_service import VehicleService
from data.repository.user_repository import UserRepository
from presentation.dto.CreateSchedule import CreateSchedule
from presentation.dto.ScheduleDetails import ScheduleDetails
from business.service.schedule_user_service import ScheduleUserService
from business.service.schedule_vehicle_service import ScheduleVehicleService
from business.service.schedule_point_service import SchedulePointService
from presentation.dto.Schedule import Schedule
from data.repository.schedule_repository import ScheduleRepository

class ScheduleService():
    schedule_repository: ScheduleRepository
    schedule_user_service: ScheduleUserService
    schedule_vehicle_service: ScheduleVehicleService
    schedule_point_service: SchedulePointService
    user_repository: UserRepository
    vehicle_service: VehicleService
    point_service: PointService

    def __init__(self):
        self.schedule_repository = ScheduleRepository()
        self.schedule_user_service = ScheduleUserService()
        self.schedule_vehicle_service = ScheduleVehicleService()
        self.schedule_point_service = SchedulePointService()
        self.user_repository = UserRepository()
        self.vehicle_service = VehicleService()
        self.point_service = PointService()

    def get_schedule_by_id(self, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_by_id(schedule_id)

        if(schedule is None):
            raise ValueError("Viagem não encontrada")

        schedule_dto = Schedule(id=schedule.id, name=schedule.name, initial_date=schedule.initial_date,
                                end_date=schedule.end_date, real_initial_date=schedule.real_initial_date,
                                real_end_date=schedule.real_end_date, description=schedule.description,
                                schedule_type_id=schedule.schedule_type_id, creation_user=schedule.creation_user)

        return schedule_dto
    
    def get_schedule_details_by_schedule_id(self, schedule_id: int):
        schedule = self.get_schedule_by_id(schedule_id)

        schedule_user = self.schedule_user_service.get_user_by_schedule_id(schedule_id)

        schedule_vehicle = self.schedule_vehicle_service.get_vehicle_by_schedule_id(schedule_id)

        schedule_points = self.schedule_point_service.get_points_by_schedule_id(schedule_id)

        schedule_details = ScheduleDetails(schedule=schedule, driver=schedule_user, 
                                           vehicle=schedule_vehicle, points=schedule_points)

        return schedule_details
    
    def create_schedule(self, schedule: CreateSchedule):
        driver = self.validate_create_schedule(schedule)

        vehicle = self.vehicle_service.get_vehicle_by_driver(driver.id)

        if(vehicle is None):
            raise ValueError("Motorista não possui veículo")
        
        students_points = self.point_service.get_point_user_id(driver.id)

        if(len(students_points) == 0):
            raise ValueError("Viagem não possuí nenhum ponto de parada")

        school = self.point_service.get_school_by_user(driver.id)

        if(school is None):
            raise ValueError("Motorista não possui escola")

        if(schedule.schedule_type == 1):
            return self.schedule_repository.create_schedule_destiny_school(schedule, driver, vehicle, students_points, school)
        elif(schedule.schedule_type == 2):
            return self.schedule_repository.create_schedule_origin_school(schedule, driver, vehicle, students_points, school)
        else:
            raise ValueError("Tipo de viagem inválida")

    def validate_create_schedule(self, schedule: CreateSchedule):
        user = self.user_repository.get_user(schedule.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário não é um motorista")
        
        return user        
    
    def create_schedule_origin_school(self, schedule: CreateSchedule):
        driver = self.validate_create_schedule(schedule)

        vehicle = self.vehicle_service.get_vehicle_by_driver(driver.id)

        if(vehicle is None):
            raise ValueError("Motorista não possui veículo")
        
        students_points = self.point_service.get_point_user_id(driver.id)

        school = self.point_service.get_school_by_user(driver.id)

        if(len(students_points) == 0):
            raise ValueError("Viagem não possuí nenhum ponto de parada")

        return 