from datetime import datetime
from typing import List
from presentation.dto.ScheduleResponsibleDetail import ScheduleResponsibleDetail
from data.repository.schedule_maps_infos_repository import ScheduleMapsInfosRepository
from presentation.dto.Student import Student
from presentation.dto.HomePoint import HomePoint
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from presentation.dto.StartSchedule import StartSchedule
from presentation.dto.Point import Point
from presentation.dto.ScheduleCreated import ScheduleCreated
from business.service.student_service import StudentService
from business.service.user_point_service import UserPointService
from business.service.user_student_service import UserStudentService
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
    user_student_service: UserStudentService
    student_service: StudentService
    user_point_service: UserPointService
    schedule_maps_infos_repository: ScheduleMapsInfosRepository

    def __init__(self):
        self.schedule_repository = ScheduleRepository()
        self.schedule_user_service = ScheduleUserService()
        self.schedule_vehicle_service = ScheduleVehicleService()
        self.schedule_point_service = SchedulePointService()
        self.user_repository = UserRepository()
        self.vehicle_service = VehicleService()
        self.point_service = PointService()
        self.user_student_service = UserStudentService()
        self.user_point_service = UserPointService()
        self.student_service = StudentService()
        self.schedule_maps_infos_repository = ScheduleMapsInfosRepository()

    def get_schedule_by_id(self, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_by_id(schedule_id)

        if(schedule is None):
            raise ValueError("Viagem não encontrada")

        schedule_dto = Schedule(id=schedule.id, name=schedule.name, initial_date=schedule.initial_date,
                                end_date=schedule.end_date, real_initial_date=schedule.real_initial_date,
                                real_end_date=schedule.real_end_date, description=schedule.description,
                                schedule_type_id=schedule.schedule_type_id, creation_user=schedule.creation_user)

        return schedule_dto
    
    def get_driver_schedule_details_by_schedule_id(self, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_id)

        if schedule is None:
            raise ValueError("Viagem não está em andamento")
        
        schedule_dto = Schedule(id=schedule.id, name=schedule.name, initial_date=schedule.initial_date,
                                end_date=schedule.end_date, real_initial_date=schedule.real_initial_date,
                                real_end_date=schedule.real_end_date, description=schedule.description,
                                schedule_type_id=schedule.schedule_type_id, creation_user=schedule.creation_user)

        schedule_user = self.schedule_user_service.get_user_by_schedule_id(schedule_id)

        schedule_vehicle = self.schedule_vehicle_service.get_vehicle_by_schedule_id(schedule_id)

        schedule_points = self.schedule_point_service.get_points_by_schedule_id(schedule_id)

        schedule_details = ScheduleDetails(schedule=schedule_dto, driver=schedule_user, 
                                           vehicle=schedule_vehicle, points=schedule_points)

        return schedule_details
    
    def get_responsible_schedule_details_by_schedule_id(self, schedule_id: int, user_id: int):
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_id)

        if schedule is None:
            raise ValueError("Viagem não está em andamento")
        
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        schedule_points = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule.id)

        if len(schedule_points) == 0:
            raise ValueError("Não existem pontos para esta viagem")

        schedule_points_points_ids = []

        for schedule_point in schedule_points:
            schedule_points_points_ids.append(schedule_point.point_id)

        user_home = self.point_service.get_point_home_by_user_id(user.id)

        if user_home is None:
            raise ValueError("Usuário não possui endereço")

        if user_home.id not in schedule_points_points_ids:
            raise ValueError("Viagem inválida")
        
        students = self.student_service.get_students_by_responsible(user.id)

        students_in_home_dto : List[Student] = []
        students_in_other_home_dto : List[Student] = []

        for student in students:
            if student.point_id == user_home.id:
                students_in_home_dto.append(Student(id=student.id, name=student.name, year=student.year, 
                                                 code=student.code, point_id=student.point_id, creation_user=student.creation_user))
            else:
                students_in_other_home_dto.append(Student(id=student.id, name=student.name, year=student.year, 
                                                 code=student.code, point_id=student.point_id, creation_user=student.creation_user))

        driver = self.schedule_user_service.get_user_by_schedule_id(schedule.id)

        vehicle = self.schedule_vehicle_service.get_vehicle_by_schedule_id(schedule.id)

        return ScheduleResponsibleDetail(point=user_home, students_in_home=students_in_home_dto, students_in_other_home=students_in_other_home_dto, driver=driver, vehicle=vehicle)
    
    def get_schedule_by_user(self, user_id: int):
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        user_students = self.user_student_service.get_students_by_responsible(user.id)

        student_ids = []
        for user_student in user_students:
            student_ids.append(user_student.student_id)

        students = self.student_service.get_students_by_list(student_ids)

        point_from_students = []
        for student in students:
            point_from_students.append(student.point_id)

        current_schedules = self.schedule_point_service.get_current_schedule_list_by_point_list(point_from_students)

        return current_schedules

    def create_schedule(self, schedule: CreateSchedule):
        driver = self.validate_create_schedule(schedule)

        vehicle_list = self.vehicle_service.get_vehicle_list_by_driver(driver.id)

        if(len(vehicle_list) == 0):
            raise ValueError("Motorista não possui veículo")

        vehicle_id_list = []
        for vehicle_db in vehicle_list:
            vehicle_id_list.append(vehicle_db.id)
 
        vehicle = self.vehicle_service.get_vehicle_by_id(schedule.vehicle_id)

        if vehicle is None:
            raise ValueError("Veículo inválido")
        
        if vehicle.id not in vehicle_id_list:
            raise ValueError("Veículo não autorizado")
        
        driver_student_list = self.user_student_service.get_students_by_responsible(driver.id)

        student_list = []

        for driver_student in driver_student_list:
            student_id = driver_student.student_id
            student_list.append(student_id)

        student_point_list = []

        students = self.student_service.get_students_by_list(student_list)

        for student in students:
            student_point_list.append(student.point_id)

        students_points = self.get_points_by_student_list(student_list, student_point_list)
        
        if(len(students_points) == 0):
            raise ValueError("Viagem não possuí nenhum ponto de parada")

        school_list = self.point_service.get_all_school_by_user(driver.id)

        if(len(school_list) == 0):
            raise ValueError("Motorista não possui escola")
        
        school_id_list = []
        for school_db in school_list:
            school_id_list.append(school_db.id)

        school = self.point_service.get_point(schedule.school_id)

        if school is None:
            raise ValueError("Escola inválida")
        
        if school.point_type_id == 1:
            raise ValueError("Este ponto não é uma escola")
        
        if school.id not in school_id_list:
            raise ValueError("Escola não associada")

        school_dto = Point(id=school.id, name=school.name, address=school.address, lat=school.lat, lng=school.lng, 
                           alt=school.alt, city=school.city, neighborhood=school.neighborhood, state=school.state,
                           description=school.description, point_type_id=school.point_type_id)

        schedule_id = 0

        if(schedule.schedule_type == 1):
            schedule_id = self.schedule_repository.create_schedule_destiny_school(schedule, driver, vehicle, school)
        elif(schedule.schedule_type == 2):
            schedule_id = self.schedule_repository.create_schedule_origin_school(schedule, driver, vehicle, school)
        else:
            raise ValueError("Tipo de viagem inválida")
        
        if schedule_id == 0:
            raise ValueError("Houve um erro ao criar a viagem")
        
        schedule_created = ScheduleCreated(points=students_points, school=school_dto, schedule_id=schedule_id)

        return schedule_created

    def validate_create_schedule(self, schedule: CreateSchedule):
        user = self.user_repository.get_user(schedule.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário não é um motorista")
        
        return user
    
    def put_schedule_start(self, start: StartSchedule):
        user = self.user_repository.get_user(start.user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        school_list = self.point_service.get_all_school_by_user(start.user_id)

        if(len(school_list) == 0):
            raise ValueError("Motorista não possui escola")
        
        school_id_list = []
        for school_db in school_list:
            school_id_list.append(school_db.id)

        school = self.point_service.get_point(start.school_id)

        if school is None:
            raise ValueError("Escola inválida")
        
        if school.point_type_id == 1:
            raise ValueError("Este ponto não é uma escola")
        
        if school.id not in school_id_list:
            raise ValueError("Escola não associada")

        self.schedule_repository.put_schedule_start(start, school)

    def put_schedule_point(self, schedule_point: PutSchedulePoint):
        user = self.user_repository.get_user(schedule_point.user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_point.schedule_id)

        if schedule is None:
            raise ValueError("Viagem não está em andamento")
        
        schedule_user = self.schedule_user_service.get_schedule_user_by_schedule_id(schedule_point.schedule_id)

        if schedule_user is None:
            raise ValueError("Não existe motorista para a viagem")
        
        if schedule_user.user_id != schedule_point.user_id:
            raise ValueError("Usuário não autorizado")
        
        schedule_point_db = self.schedule_point_service.get_schedule_point_by_id(schedule_point.schedule_point_id)

        if schedule_point_db is None:
            raise ValueError("Ponto não identificado")

        schedules_point_list_db = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule_point.schedule_id)

        scheduls_points_id_list_db = []
        for schedule_point_id in schedules_point_list_db:
            scheduls_points_id_list_db.append(schedule_point_id.id)

        if schedule_point_db.id not in scheduls_points_id_list_db:
            raise ValueError("Ponto não autorizado")

        point = self.point_service.get_point(schedule_point_db.point_id)

        if point is None:
            raise ValueError("Ponto inválido")
        
        if point.point_type_id == 2:
            raise ValueError("Ponto não autorizado")

        self.schedule_point_service.put_schedule_point(schedule_point.schedule_point_id, schedule_point.user_id)

    def put_schedule_end(self, schedule_id: int, user_id: int):
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")
        
        schedule_user = self.schedule_user_service.get_schedule_user_by_schedule_id(schedule_id)

        if schedule_user.user_id != user_id:
            raise ValueError("Usuário não autorizado")
        
        schedule_point = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule_id)
        
        self.schedule_repository.put_schedule_end(schedule, user_id)

    def get_schedule_student_position(self, schedule_id: int, user_id: int):
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")
        
        schedule_points = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule.id)

        if len(schedule_points) == 0:
            raise ValueError("Não existem pontos para esta viagem")

        schedule_points_points_ids = []
        schedule_points_already_completed = 1

        for schedule_point in schedule_points:
            schedule_points_points_ids.append(schedule_point.point_id)
            if(schedule_point.real_date != None):
                schedule_points_already_completed += 1

        user_home = self.point_service.get_point_home_by_user_id(user.id)

        if user_home is None:
            raise ValueError("Usuário não possui endereço")

        if user_home.id not in schedule_points_points_ids:
            raise ValueError("Viagem inválida")
        
        user_home_in_schedule_order = 0

        for schedule_point in schedule_points:
            if(schedule_point.point_id == user_home.id):
                user_home_in_schedule_order = schedule_point.order
        
        if user_home_in_schedule_order < schedule_points_already_completed:
            raise ValueError("Seu estudante já embarcou")
        
        return user_home_in_schedule_order - schedule_points_already_completed

    def get_schedule_maps_infos(self, schedule_id: int, user_id: int):
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")
        
        return self.schedule_maps_infos_repository.get_schedule_maps_infos_by_schedule_id(schedule.id)

    def get_points_by_student_list(self, student_ids: List[int], student_point_ids: List[int]):
        home_point_list: List[HomePoint] = []
        students_dto : List[Student] = []

        points : List[Point] = self.point_service.get_point_home_list_by_user(student_point_ids)

        students = self.student_service.get_students_by_list(student_ids)

        for student in students:
            students_dto.append(Student(id=student.id, name=student.name, year=student.year, code=student.code,
                                        point_id=student.point_id, creation_user=student.creation_user))
            
        for point in points:
            student_dto_list = []
            for student_dto in students_dto:
                if(student_dto.point_id == point.id):
                    student_dto_list.append(student_dto)
            
            home_point = HomePoint(point=point, student=student_dto_list)
            home_point_list.append(home_point)

        return home_point_list