from data.model.student_model import StudentModel
from data.repository.user_phone_repository import UserPhoneRepository
from data.repository.student_repository import StudentRepository
from business.service.user_student_service import UserStudentService
from presentation.dto.Vehicle import Vehicle
from data.repository.vehicle_point_repository import VehiclePointRepository
from data.repository.user_repository import UserRepository
from business.service.user_phone_service import UserPhoneService
from business.service.point_service import PointService
from business.service.user_point_service import UserPointService
from presentation.dto.CreateUser import CreateUser
from data.model.user_model import UserModel
from data.repository.vehicle_repository import VehicleRepository
from presentation.dto.CreatePoint import CreatePoint
from presentation.dto.User import User
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.DriverDetails import DriverDetails
from presentation.dto.Point import Point
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from presentation.dto.UpdateUser import UpdateUser
from presentation.dto.UserDetails import UserDetails
from validate_docbr import CPF
from typing import List
from validate_rg import validate_rg
import re

class UserService():
    user_repository: UserRepository
    user_phone_service: UserPhoneService
    user_phone_repository: UserPhoneRepository
    point_service: PointService
    user_point_service: UserPointService
    vehicle_repository: VehicleRepository
    vehicle_point_repository: VehiclePointRepository
    user_student_service: UserStudentService
    student_repository: StudentRepository

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_phone_service = UserPhoneService()
        self.point_service = PointService()
        self.user_point_service = UserPointService()
        self.vehicle_repository = VehicleRepository()
        self.vehicle_point_repository = VehiclePointRepository()
        self.user_student_service = UserStudentService()
        self.student_repository = StudentRepository()
        self.user_phone_repository = UserPhoneRepository()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
   
    def get_user_by_code(self, code: str):
        return self.user_repository.get_user_by_code(code)
    
    def get_user_list_by_list(self, user_id_list: List[int]):
        return self.user_repository.get_user_by_list(user_id_list)

    def get_all_drivers(self):
        return self.user_repository.get_all_drivers()
    
    def get_driver_detals_by_code(self, code: str):
        vehicle_point = self.vehicle_point_repository.get_vehicle_point_association_by_code(code)

        if vehicle_point is None:
            raise ValueError("Código inválido")
        
        vehicle = self.vehicle_repository.get_vehicle(vehicle_point.vehicle_id)

        if vehicle is None:
            raise ValueError("Veículo não encontrado")
        
        vehicle_dto = Vehicle(id=vehicle.id, plate=vehicle.plate, vehicle_type_id=vehicle.vehicle_type_id, color=vehicle.color,
                              model=vehicle.model, year=vehicle.year, code=vehicle.code)
        
        user_from_vehicle = self.user_repository.get_user(vehicle.user_id)

        user_dto = User(id=user_from_vehicle.id, uuid=user_from_vehicle.uuid, name=user_from_vehicle.name, email=user_from_vehicle.email, cpf=user_from_vehicle.cpf, 
                        cnh=user_from_vehicle.cnh, rg=user_from_vehicle.rg, user_type_id=user_from_vehicle.user_type_id, code=user_from_vehicle.code)

        school = self.point_service.get_school_by_id(vehicle_point.point_id)

        if school is None:
            raise ValueError("Motorista não possui escola")

        user_school_dto = Point(id=school.id, name=school.name, address=school.address, lat=school.lat,
                                lng=school.lng, alt=school.alt, city=school.city, neighborhood=school.neighborhood,
                                state=school.state, description=school.description, point_type_id=school.point_type_id)

        user_phone = self.user_phone_service.get_user_phone_list(user_from_vehicle.id)

        driver_details_dto = DriverDetails(user=user_dto, school=user_school_dto, phone=user_phone, vehicle=vehicle_dto)
    
        return driver_details_dto

    def get_drivers_without_vehicle(self):
        all_drivers = self.user_repository.get_all_drivers()

        vehicles = self.vehicle_repository.get_all_vehicle()

        drivers_with_vehicles = []

        for vehicle in vehicles:
            driver_id = vehicle.user_id
            drivers_with_vehicles.append(driver_id)

        drivers_without_vehicles = []

        for driver in all_drivers:
            if driver.id not in drivers_with_vehicles:
                drivers_without_vehicles.append(driver)
        
        return drivers_without_vehicles
    
    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)
    
    def create_user(self, user: CreateUser):
        if(user.user_type_id == 1):
            self.validate_administrator(user)
        elif(user.user_type_id == 2):
            self.validate_driver(user)
        else:
            self.validate_responsible(user)

        user_id = self.creating_user(user=user)
    
        self.creating_user_phone(user_id=user_id, phone=user.phone)

        self.creating_user_point(user_id=user_id, user_name=user.name, point=user.address)

        return user_id
      
    def update_user_uuid(self, user_data: UpdateUserUuid):
        user = self.user_repository.get_user(user_data.user_id)

        if(user == None):
            raise ValueError("Usuário não existe")
        
        return self.user_repository.update_user_uuid(user_data.user_id, user_data.uuid)
    
    def update_user(self, user_data: UpdateUser):
        self.validating_update_user(user_data)
        
        self.user_repository.update_user(user_data)

    def update_driver_code(self, user_id: int, code: str):        
        self.user_repository.update_user_code(user_id, code)
    
    def delete_user(self, user_id: int):
        user = self.validating_delete_user(user_id)
        
        user_points = self.user_point_service.get_user_point_list(user_id)

        user_phones = self.user_phone_repository.get_user_phone_list(user_id)

        user_students = self.user_student_service.get_students_by_responsible(user_id)

        student_ids = []
        for user_student in user_students:
            student_ids.append(user_student.student_id)

        students = self.student_repository.get_students_by_student_list(student_ids)

        students_created_by_this_user_ids = []
        students_only_associated : List[StudentModel] = []
        responsibles_to_students_this_user_is_associated = []

        for student in students:
            if(student.creation_user == user_id):
                students_created_by_this_user_ids.append(student.id)
            else:
                students_only_associated.append(student)
                responsibles_to_students_this_user_is_associated.append(student.creation_user)

        user_student_from_another_responsibles = self.user_student_service.get_user_students_by_student_list(students_created_by_this_user_ids)
        
        students_created_by_user = self.student_repository.get_students_by_student_list(students_created_by_this_user_ids)

        homes = self.point_service.get_points_by_user_list(responsibles_to_students_this_user_is_associated)

        students_to_update = students_only_associated
        for i, students_to_update in enumerate(students_only_associated):
            if i < len(homes):
                students_to_update.point_id = homes[i].id

        self.user_repository.delete_user(user, user_points, user_phones, user_students, user_student_from_another_responsibles, students_created_by_user, students_only_associated)

    def user_details(self, user_id: int):
        self.validating_user_detail(user_id)

        points_dto = []
        
        user = self.user_repository.get_user(user_id)

        user_dto = User(id=user.id, code=user.code, uuid=user.uuid, name=user.name, email=user.email, cpf=user.cpf, cnh=user.cnh, rg=user.rg, user_type_id=user.user_type_id)

        user_phone = self.user_phone_service.get_user_phone_list(user_id)

        user_points = self.user_point_service.get_user_point_list(user_id)
        
        if(len(user_points) > 0):
            point_id_list = []
            for user_point in user_points:
                point_id_list.append(user_point.point_id)

            points = self.point_service.get_point_list_by_user(point_id_list)

            points_dto = points

        user_details = UserDetails(user=user_dto, phone=user_phone, points=points_dto)

        return user_details
    
    def validate_responsible(self, user: CreateUser):
        self.validate_email(user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")
        
        if(user.rg != ""):
            if(self.user_repository.get_user_by_rg(user.rg) != None):
                raise ValueError("RG já cadastrado")

            if(not validate_rg.is_valid(user.rg)):
                raise ValueError("RG inválido")

    def validate_administrator(self, user: CreateUser):
        self.validate_email(user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")
        
    def validate_update_administrator(self, user: UpdateUser):
        self.validate_update_email(user.id, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")

        db_user = self.user_repository.get_user_by_cpf(user.cpf)

        if(db_user is not None and db_user.id != user.id):
            raise ValueError("CPF já cadastrado")
        
    def validate_update_responsible(self, user: UpdateUser):
        self.validate_update_email(user.id, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")

        if(not validate_rg.is_valid(user.rg)):
            raise ValueError("RG inválido")
        
        db_user_cpf = self.user_repository.get_user_by_cpf(user.cpf)

        if(db_user_cpf is not None and db_user_cpf.id != user.id):
            raise ValueError("CPF já cadastrado")
        
        db_user_rg = self.user_repository.get_user_by_rg(user.rg)

        if(db_user_rg is not None and db_user_rg.id != user.id):
            raise ValueError("RG já cadastrado")


    def validate_driver(self, user: CreateUser):
        self.validate_email(user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")

        if(self.user_repository.get_user_by_cnh(user.cnh) != None):
            raise ValueError("CNH já cadastrada")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")

        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")
        
        if(user.rg != ""):
            if(self.user_repository.get_user_by_rg(user.rg) != None):
                raise ValueError("RG já cadastrado")

            if(not validate_rg.is_valid(user.rg)):
                raise ValueError("RG inválido")
            
    def validate_update_driver(self, user: UpdateUser):
        self.validate_update_email(user.id, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")

        if(user.cnh):
            db_user_cnh = self.user_repository.get_user_by_cnh(user.cnh)

            if(db_user_cnh is not None and db_user_cnh.id != user.id):
                raise ValueError("CNH já cadastrada")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")

        if(not validate_rg.is_valid(user.rg)):
            raise ValueError("RG inválido")
        
        db_user_cpf = self.user_repository.get_user_by_cpf(user.cpf)

        if(db_user_cpf is not None and db_user_cpf.id != user.id):
            raise ValueError("CPF já cadastrado")
        
        db_user_rg = self.user_repository.get_user_by_rg(user.rg)

        if(db_user_rg is not None and db_user_rg.id != user.id):
            raise ValueError("RG já cadastrado")

    def validate_email(self, email: str):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if(self.user_repository.get_user_by_email(email) != None):
            raise ValueError("E-mail já cadastrado")
        
        if(not re.match(regex, email)):
            raise ValueError("E-mail inválido")
        
    def validate_update_email(self, id: int, email: str):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        user_by_email = self.user_repository.get_user_by_email(email)

        if(user_by_email is not None and user_by_email.id != id):
            raise ValueError("E-mail já cadastrado")
        
        if(not re.match(regex, email)):
            raise ValueError("E-mail inválido")
        
    def creating_user(self, user: CreateUser):
        user_body = UserModel(name=user.name, email=user.email, cpf=user.cpf, cnh=user.cnh, user_type_id=user.user_type_id, rg=user.rg)

        user_id = self.user_repository.create_user(user_body)

        return user_id

    def creating_user_phone(self, user_id: int, phone: str):
        phone_body = CreatePhone(user_id=user_id, phone=phone)

        self.user_phone_service.create_phone(phone_body)

    def creating_user_point(self, user_id: int, user_name: str, point : CreatePoint):
        point_id = self.point_service.create_point(point=point)

        self.user_point_service.create_user_point(user_id=user_id, point_id=point_id, is_favorite=True)

    def validating_update_user(self, user: UpdateUser):
        if(self.user_repository.get_user(user.id) is None):
            raise ValueError("Usuário não existe")
        
        if(user.user_type_id == 1):
            self.validate_update_administrator(user)
        elif(user.user_type_id == 2):
            self.validate_update_driver(user)
        else:
            self.validate_update_responsible(user)

    def validating_delete_user(self, user_id: int):
        user = self.user_repository.get_user(user_id)
        if(user is None):
            raise ValueError("Usuário não existe")
        
        return user
        
    def validating_user_detail(self, user_id : int):
        if(self.user_repository.get_user(user_id) is None):
            raise ValueError("Usuário não existe")