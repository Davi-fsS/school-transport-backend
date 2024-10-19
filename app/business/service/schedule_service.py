from datetime import date, datetime
from typing import List
from presentation.dto.ScheduleHistoricResponsible import ScheduleHistoricResponsible
from presentation.dto.ScheduleHistoricDetails import ScheduleHistoricDetails
from presentation.dto.SchedulePoint import SchedulePoint
from presentation.dto.Coordinate import Coordinate
from data.repository.coordinate_repository import CoordinateRepository
from presentation.dto.ScheduleHistoric import ScheduleHistoric
from business.service.parent_notification_service import ParentNotificationService
from data.model.student_model import StudentModel
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
    parent_notification_service: ParentNotificationService
    coordinate_repository: CoordinateRepository

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
        self.parent_notification_service = ParentNotificationService()
        self.coordinate_repository = CoordinateRepository()

    def get_schedule_by_id(self, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_by_id(schedule_id)

        if(schedule is None):
            raise ValueError("Viagem não encontrada")

        schedule_dto = Schedule(id=schedule.id, name=schedule.name, initial_date=schedule.initial_date,
                                end_date=schedule.end_date, real_initial_date=schedule.real_initial_date,
                                real_end_date=schedule.real_end_date, description=schedule.description,
                                schedule_type_id=schedule.schedule_type_id, creation_user=schedule.creation_user)

        return schedule_dto
    
    def get_schedule_by_student(self, student_id: int, user_id: int):
        self.validating_responsible(user_id)

        driver_by_student = self.student_service.get_student_driver(student_id)

        if driver_by_student is None:
            raise ValueError("Este aluno não possuí um motorista")
        
        driver_schedule = self.schedule_user_service.get_current_schedule_by_user(driver_by_student.id)

        if driver_schedule is None:
            raise ValueError("Não possuí viagem em andamento")

        parent_notificaton_to_student = self.parent_notification_service.get_parent_notification_list_by_student_today(student_id)

        if(len(parent_notificaton_to_student) == 0):
            return driver_schedule

        for notification in parent_notificaton_to_student:
            if(notification.parent_notification_period_id == driver_schedule.schedule_type_id or 
               notification.parent_notification_period_id == 3):
                raise ValueError("Este aluno não está utilizando o transporte no momento")

        return driver_schedule

    def get_schedule_in_progress(self, schedule_id: int):
        return self.schedule_repository.get_schedule_in_progress(schedule_id)

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
    
    def get_schedule_by_driver(self, user_id: int):
        driver = self.validating_driver(user_id)

        current_schedule_by_driver = self.schedule_user_service.get_current_schedule_by_user(driver.id)

        if current_schedule_by_driver is None:
            return None

        schedule_dto = Schedule(id=current_schedule_by_driver.id, name=current_schedule_by_driver.name, initial_date=current_schedule_by_driver.initial_date,
                                end_date=current_schedule_by_driver.end_date, real_initial_date=current_schedule_by_driver.real_initial_date,
                                real_end_date=current_schedule_by_driver.real_end_date, description=current_schedule_by_driver.description, 
                                schedule_type_id=current_schedule_by_driver.schedule_type_id, creation_user=current_schedule_by_driver.creation_user)

        return schedule_dto

    def create_schedule(self, schedule: CreateSchedule):
        driver = self.validating_driver(schedule.user_id)

        vehicle = self.validating_vehicle(driver.id, schedule.vehicle_id)

        school, school_dto = self.validating_school(driver.id, schedule.school_id)

        student_list, students_active, students_inactive = self.listing_driver_students(driver.id, schedule.schedule_type)

        students_points = self.listing_students_points(students_active, student_list)

        schedule_id = self.schedule_repository.create_schedule(schedule, driver, vehicle, school)
        
        schedule_created = ScheduleCreated(points=students_points, school=school_dto, schedule_id=schedule_id, students_inactive=students_inactive)

        return schedule_created
    
    def put_schedule_start(self, start: StartSchedule):
        self.validating_driver(start.user_id)

        schedule = self.validating_driver_on_not_started_schedule(start.user_id, start.schedule_id)

        school, _ = self.validating_school(start.user_id, start.school_id)

        destiny = None

        if(schedule.schedule_type_id == 2):
            destiny = self.validating_destiny_schedule(start.user_id, start.destiny_id)

        self.schedule_repository.put_schedule_start(start, school, destiny)

    def put_schedule_point(self, schedule_point: PutSchedulePoint):
        self.validating_driver(schedule_point.user_id)
        
        self.validating_driver_on_current_schedule(schedule_point.user_id, schedule_point.schedule_id)
                
        self.validating_point_to_embark(schedule_point.schedule_id, schedule_point.point_id)

        self.schedule_point_service.put_schedule_point(schedule_point.schedule_id, schedule_point.point_id, schedule_point.user_id, schedule_point.has_embarked)

    def validating_destiny_schedule(self, driver_id: int, destiny_id: int):
        driver_point_list = self.user_point_service.get_user_point_list(driver_id)

        driver_point_ids = []
        for driver_point in driver_point_list:
            driver_point_ids.append(driver_point.point_id)

        if(destiny_id not in driver_point_ids):
            raise ValueError("Destino não permitido")
        
        destiny = self.point_service.get_point_by_id(destiny_id)

        if destiny is None:
            raise ValueError("Destino inválido")
        
        return destiny

    def put_schedule_end(self, schedule_id: int, user_id: int):
        self.validating_driver(user_id)
        
        schedule = self.validating_driver_on_current_schedule(user_id, schedule_id)

        self.validating_schedule_last_point(schedule_id)
        
        self.schedule_repository.put_schedule_end(schedule, user_id)

    def get_schedule_driver_historic_details(self, schedule_id: int, user_id: int):
        self.validating_driver(user_id)

        schedule = self.schedule_repository.get_schedule_by_id(schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")
        
        schedule_user = self.schedule_user_service.get_schedule_user_by_schedule_id(schedule.id)

        if schedule_user.user_id != user_id:
            raise ValueError("Motorista não está nessa viagem")

        schedule_points = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule_id)

        schedule_points_dto : List[SchedulePoint] = []
        point_ids = []

        for schedule_point in schedule_points:
            point_ids.append(schedule_point.point_id)

        points = self.point_service.get_point_list_by_list(point_ids)

        for schedule_point in schedule_points:
            point_dto = list(filter(lambda point: point.id == schedule_point.point_id, points))[0]

            schedule_points_dto.append(SchedulePoint(id=schedule_point.id, planned_date=schedule_point.planned_date,
                                                     real_date=schedule_point.real_date, order=schedule_point.order,
                                                     schedule_id=schedule_point.schedule_id, has_embarked=schedule_point.has_embarked,
                                                     creation_user=schedule_point.creation_user, point=point_dto))
            
        end_date = schedule.end_date

        if(end_date is None):
            end_date = datetime.now()

        duration = end_date - schedule.initial_date

        duration_in_datetime = datetime.min + duration

        real_end_date = schedule.real_end_date

        if(real_end_date is None):
            real_end_date = datetime.now()

        real_duration = real_end_date - schedule.real_initial_date

        real_duration_in_datetime = datetime.min + real_duration

        schedule_type = "Ida"

        if schedule.schedule_type_id == 2:
            schedule_type = "Volta"

        schedule_driver_historic_dto = ScheduleHistoricDetails(real_duration=real_duration_in_datetime, planned_duration=duration_in_datetime, 
                                                               id=schedule.id, initial_date=schedule.initial_date, end_date=schedule.end_date,
                                                                real_initial_date=schedule.real_initial_date, real_end_date=schedule.real_end_date,
                                                                name=schedule.name, schedule_type=schedule_type, points=schedule_points_dto)

        return schedule_driver_historic_dto

    def get_schedule_responsible_historic_by_date(self, data: str, user_id: int):
        schedule_historic : List[ScheduleHistoricResponsible] = []

        self.validating_responsible(user_id)

        student_list = self.student_service.get_students_by_responsible(user_id)

        student_list_ids = []
        for student in student_list:
            student_list_ids.append(student.id)

        others_responsibles_to_students = self.user_student_service.get_responsibles_by_student_list(student_list_ids)

        others_responsibles_ids = []

        for responsible in others_responsibles_to_students:
            others_responsibles_ids.append(responsible.id)

        user_points = self.user_point_service.get_user_point_list_by_user_list(others_responsibles_ids)

        point_list = []

        for user_point in user_points:
            point_list.append(user_point.point_id)

        points_by_responsibles = self.point_service.get_point_home_list_by_user(point_list)

        points_ids = []

        for point in points_by_responsibles:
            points_ids.append(point.id)

        date_format = datetime.strptime(data, "%Y-%m-%d").date()

        schedules_points_from_date = self.schedule_point_service.get_schedule_point_list_by_point_list_date(points_ids, date_format)

        schedule_ids = []
        points_in_schedule_ids = []
        for schedule_point in schedules_points_from_date:
            if(schedule_point.schedule_id not in schedule_ids):
                schedule_ids.append(schedule_point.schedule_id)

            if(schedule_point.point_id not in points_in_schedule_ids):
                points_in_schedule_ids.append(schedule_point.point_id)
        
        schedules = self.schedule_repository.get_schedule_list_by_list(schedule_ids)

        points = self.point_service.get_point_list_by_list(points_in_schedule_ids)

        for schedule_point in schedules_points_from_date:
            schedule = list(filter(lambda sched: sched.id == schedule_point.schedule_id, schedules))[0]

            schedule_dto = Schedule(id=schedule.id, name=schedule.name, initial_date=schedule.initial_date, end_date=schedule.end_date,
                                    real_initial_date=schedule.real_initial_date, real_end_date=schedule.real_end_date, description=schedule.description,
                                    schedule_type_id=schedule.schedule_type_id, creation_user=schedule.creation_user)

            if schedule is not None:
                point_dto = list(filter(lambda poi: poi.id == schedule_point.point_id, points))

                schedule_historic_item = ScheduleHistoricResponsible(schedule=schedule_dto, points=point_dto, coordinates=None)

                schedule_historic.append(schedule_historic_item)

        return schedule_historic

    def get_schedule_driver_historic_by_date(self, date: str, user_id: int) -> List[ScheduleHistoric]:
        schedule_historic : List[ScheduleHistoric] = []

        self.validating_driver(user_id)

        schedules_by_driver = self.schedule_user_service.get_schedule_user_list_by_user_id(user_id)

        if len(schedules_by_driver) == 0:
            raise ValueError("Não existe nenhuma viagem")
        
        all_schedule_drivers_id = []
        for schedule_driver in schedules_by_driver:
            all_schedule_drivers_id.append(schedule_driver.schedule_id)

        date_format = datetime.strptime(date, "%Y-%m-%d").date()

        schedules_from_date = self.schedule_repository.get_schedule_list_by_list_and_date(all_schedule_drivers_id, date_format)

        if len(schedules_from_date) == 0:
            raise ValueError("Não existe viagem para esta data")
        
        schedules_ids = []
        
        for schedule_date in schedules_from_date:
            schedules_ids.append(schedule_date.id)
        
        coordinates_from_schedules = self.coordinate_repository.get_list_coordinates_by_schedule_list(schedules_ids)

        lora_coordinates_from_schedules = self.coordinate_repository.get_list_lora_coordinates_by_schedule_list(schedules_ids)

        for schedule_date in schedules_from_date:
            coordinate_dto : List[Coordinate] = []
            lora_coordinate_dto: List[Coordinate] = []
            coordinates_to_schedule = list(filter(lambda coord: coord.schedule_id == schedule_date.id, coordinates_from_schedules))

            lora_coordinates_from_schedule = list(filter(lambda coord: coord.schedule_id == schedule_date.id, lora_coordinates_from_schedules))

            schedule_dto = Schedule(id=schedule_date.id, name=schedule_date.name, initial_date=schedule_date.initial_date, end_date=schedule_date.end_date,
                                real_initial_date=schedule_date.real_initial_date, real_end_date=schedule_date.real_end_date, description=schedule_date.description,
                                schedule_type_id=schedule_date.schedule_type_id, creation_user=schedule_date.creation_user)
        
            for coordinate in coordinates_to_schedule:
                coordinate_dto.append(Coordinate(lat=coordinate.lat, lng=coordinate.lng, coordinate_type_id=coordinate.coordinate_type_id,
                                                 schedule_id=coordinate.schedule_id, register_date=coordinate.register_date, creation_user=coordinate.creation_user))
            
            for lora_coordinate in lora_coordinates_from_schedule:
                lora_coordinate_dto.append(Coordinate(lat=lora_coordinate.lat, lng=lora_coordinate.lng, coordinate_type_id=lora_coordinate.coordinate_type_id,
                                                 schedule_id=lora_coordinate.schedule_id, register_date=lora_coordinate.register_date, creation_user=lora_coordinate.creation_user))

            schedule_historic.append(ScheduleHistoric(schedule=schedule_dto, coordinates=coordinate_dto, coordinates_lora=lora_coordinate_dto))
        
        return schedule_historic

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
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
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
            
            home_point = HomePoint(point=point, student=student_dto_list, status=None)
            home_point_list.append(home_point)

        return home_point_list
    
    def get_responsibles_in_schedule(self, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_by_id(schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")

        schedule_points = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule.id)

        if len(schedule_points) == 0:
            raise ValueError("Não há pontos para essa viagem")
        
        point_id_list = []

        for schedule_point in schedule_points:
            point_id_list.append(schedule_point.point_id)

        students = self.student_service.get_students_by_point_list(point_id_list)

        student_id_list = []

        for student in students:
            student_id_list.append(student.id)

        return self.user_student_service.get_responsibles_by_student_list(student_id_list)
    
    def validating_driver(self, user_id: int):
        user = self.user_repository.get_user(user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário não é um motorista")
        
        return user
    
    def validating_responsible(self, user_id: int):
        user = self.user_repository.get_user(user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 2):
            raise ValueError("Usuário não é um responsável")
        
        return user

    def validating_vehicle(self, driver_id: int, vehicle_id: int):
        vehicle_list = self.vehicle_service.get_vehicle_list_by_driver(driver_id)

        if(len(vehicle_list) == 0):
            raise ValueError("Motorista não possui veículo")

        vehicle_id_list = []
        for vehicle_db in vehicle_list:
            vehicle_id_list.append(vehicle_db.id)
 
        vehicle = self.vehicle_service.get_vehicle_by_id(vehicle_id)

        if vehicle is None:
            raise ValueError("Veículo inválido")
        
        if vehicle.id not in vehicle_id_list:
            raise ValueError("Veículo não autorizado")
        
        return vehicle
    
    def listing_driver_students(self, driver_id: int, schedule_type_id: int):
        driver_student_list = self.user_student_service.get_students_by_responsible(driver_id)

        student_list = []

        for driver_student in driver_student_list:
            student_id = driver_student.student_id
            student_list.append(student_id)

        student_actives, students_active, students_inactive = self.listing_active_students(student_list, schedule_type_id)

        return student_actives, students_active, students_inactive
    
    def listing_active_students(self, student_list : List[int], schedule_type_id: int):
        parent_notifications = self.parent_notification_service.get_parent_notification_list_by_student_list_today(student_list)

        students_inative = []

        for parent_notification in parent_notifications:
            if(parent_notification.student_id in student_list):
                if(parent_notification.parent_notification_period_id == 1 and schedule_type_id == 1):
                    students_inative.append(parent_notification.student_id)
                elif(parent_notification.parent_notification_period_id == 2 and schedule_type_id == 2):
                    students_inative.append(parent_notification.student_id)
                elif(parent_notification.parent_notification_period_id == 3):
                    students_inative.append(parent_notification.student_id)

        students_active = []

        for student in student_list:
            if(student not in students_inative):
                students_active.append(student)

        students_actives = self.student_service.get_students_by_list(students_active)

        students_inactive_list = self.student_service.get_students_by_list(students_inative)

        students_inactive_dto : List[Student] = []

        for student_inactive in students_inactive_list:
            students_inactive_dto.append(Student(id=student_inactive.id, name=student_inactive.name, year=student_inactive.year,
                                                 code=student_inactive.code, point_id=student_inactive.point_id, creation_user=student_inactive.creation_user))

        return students_active, students_actives, students_inactive_dto

    def listing_students_points(self, students_active : List[StudentModel], student_list: List[int]): 
        student_point_list = []

        for student in students_active:
            student_point_list.append(student.point_id)

        students_points = self.get_points_by_student_list(student_list, student_point_list)
        
        if(len(students_points) == 0):
            raise ValueError("Viagem não possuí nenhum ponto de parada")
        
        return students_points
    
    def validating_school(self, driver_id: int, school_id: int):
        school_list = self.point_service.get_all_school_by_user(driver_id)

        if(len(school_list) == 0):
            raise ValueError("Motorista não possui escola")
        
        school_id_list = []
        for school_db in school_list:
            school_id_list.append(school_db.id)

        school = self.point_service.get_point(school_id)

        if school is None:
            raise ValueError("Escola inválida")
        
        if school.point_type_id == 1:
            raise ValueError("Este ponto não é uma escola")
        
        if school.id not in school_id_list:
            raise ValueError("Escola não associada")

        school_dto = Point(id=school.id, name=school.name, address=school.address, lat=school.lat, lng=school.lng, 
                           alt=school.alt, city=school.city, neighborhood=school.neighborhood, state=school.state,
                           description=school.description, point_type_id=school.point_type_id)
        
        return school, school_dto

    def validating_driver_on_not_started_schedule(self, driver_id: int, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_not_started(schedule_id)
        
        if schedule is None:
            raise ValueError("Viagem inválida")
        
        schedule_driver = self.schedule_user_service.get_schedule_user_by_schedule_id(schedule.id)

        if schedule_driver is None:
            raise ValueError("A viagem não possuí motorista")
        
        if schedule_driver.user_id != driver_id:
            raise ValueError("O motorista não pertence à essa viagem")
        
        return schedule
        
    def validating_driver_on_current_schedule(self, driver_id: int, schedule_id: int):
        schedule = self.schedule_repository.get_schedule_in_progress(schedule_id)

        if schedule is None:
            raise ValueError("Viagem não está em andamento")

        schedule_user = self.schedule_user_service.get_schedule_user_by_schedule_id(schedule_id)

        if schedule_user is None:
            raise ValueError("Não existe motorista para a viagem")
        
        if schedule_user.user_id != driver_id:
            raise ValueError("Usuário não autorizado")
        
        return schedule
        
    def validating_point_to_embark(self, schedule_id: int, point_id: int):
        schedule_point_db = self.schedule_point_service.get_schedule_point_by_point_id(schedule_id, point_id)

        if schedule_point_db is None:
            raise ValueError("Ponto não identificado")
        
        if schedule_point_db.real_date != None:
            raise ValueError("Ponto já passado")

        schedules_point_list_db = self.schedule_point_service.get_schedule_point_by_schedule_id(schedule_id)

        scheduls_points_id_list_db = []
        schedule_point_not_visited = []
        for schedule_point_id in schedules_point_list_db:
            scheduls_points_id_list_db.append(schedule_point_id.point_id)

            if(schedule_point_id.real_date == None and schedule_point_id.has_embarked == None):
                schedule_point_not_visited.append(schedule_point_id)

        if schedule_point_not_visited[0].id != schedule_point_db.id:
            raise ValueError("Este não é o ponto atual")

        if schedule_point_db.point_id not in scheduls_points_id_list_db:
            raise ValueError("Ponto não autorizado")

        point = self.point_service.get_point(schedule_point_db.point_id)

        if point is None:
            raise ValueError("Ponto inválido")
        
        if point.point_type_id == 2:
            raise ValueError("Ponto não autorizado")
        
    def validating_schedule_last_point(self, schedule_id: int):
        actual_schedule_point = self.schedule_point_service.get_current_schedule_point_by_schedule_id(schedule_id)

        last_point = self.schedule_point_service.get_last_schedule_point(schedule_id)

        if actual_schedule_point.id != last_point.id:
            raise ValueError("Não é possível finalizar a viagem até que todos as paradas sejam informadas")