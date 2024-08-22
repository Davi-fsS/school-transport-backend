from data.repository.vehicle_repository import VehicleRepository
from business.service.user_service import UserService
from business.service.vehicle_type_service import VehicleTypeService
from data.model.vehicle_model import VehicleModel
from data.model.user_model import UserModel
from presentation.dto.CreateVehicle import CreateVehicle
from presentation.dto.UpdateVehicle import UpdateVehicle
from presentation.dto.VehicleUser import VehicleUser
from typing import List

class VehicleService():
    vehicle_repository: VehicleRepository
    user_service: UserService
    vehicle_type_service: VehicleTypeService

    def __init__(self):
        self.vehicle_repository = VehicleRepository()
        self.user_service = UserService()
        self.vehicle_type_service = VehicleTypeService()

    def get_vehicle_by_id(self, vehicle_id: int):
        return self.vehicle_repository.get_vehicle(vehicle_id)

    def get_all_vehicle(self):
        all_vehicles = self.vehicle_repository.get_all_vehicle()

        if(len(all_vehicles) == 0):
            raise ValueError("Não existe nenhum veículo")

        user_id_list = self.get_user_list_by_vehicles(all_vehicles)

        user_list = self.user_service.get_user_list_by_list(user_id_list)

        all_vehicles_dto : List[VehicleUser] = []
    
        for vehicle in all_vehicles:
            user = list(filter(lambda user: user.id == vehicle.user_id, user_list))[0]

            vehicle_user = VehicleUser(
                id = vehicle.id,
                plate = vehicle.plate,
                model=vehicle.model,
                color=vehicle.color,
                year=vehicle.year,
                user_id=user.id,
                user_name=user.name
            )

            all_vehicles_dto.append(vehicle_user)

        return all_vehicles_dto
    
    def get_user_list_by_vehicles(self, all_vehicles: List[VehicleModel]):
        user_id_list = []

        for vehicle in all_vehicles:
            user_id = vehicle.user_id
            user_id_list.append(user_id)

        return user_id_list

    def create_vehicle(self, vehicle: CreateVehicle):
        driver = self.validating_vehicle_create(vehicle)

        code = self.creating_driver_code(driver, vehicle)

        vehicle_model = VehicleModel(plate=vehicle.plate, 
                                     vehicle_type_id=vehicle.vehicle_type_id,
                                     user_id=vehicle.user_id,
                                     model=vehicle.model,
                                     color=vehicle.color,
                                     year=vehicle.year,
                                     creation_user = 2,
                                     code=code
                                    )
        
        return self.vehicle_repository.create_vehicle(vehicle_model)
    
    def update_vehicle(self, vehicle: UpdateVehicle):
        driver = self.validating_vehicle_update(vehicle)

        code = self.creating_driver_code(driver, vehicle)

        return self.vehicle_repository.update_vehicle(vehicle, code)

    def delete_vehicle(self, vehicle_id: int):
        vehicle = self.validating_vehicle_delete(vehicle_id)

        self.user_service.update_driver_code(vehicle.user_id, None)

        return self.vehicle_repository.delete_vehicle(vehicle_id)

    def get_vehicle_by_driver(self, user_id: int):
        self.validating_vehicle_by_driver(user_id)

        return self.vehicle_repository.get_vehicle_by_driver(user_id)

    def validating_vehicle_create(self, vehicle: CreateVehicle):
        if(len(vehicle.plate) != 7):
            raise ValueError("Placa incorreta")
        
        if(self.vehicle_repository.get_vehicle_by_plate(vehicle.plate) is not None):
            raise ValueError("Veículo já registrado")
        
        user = self.user_service.get_user(vehicle.user_id)

        if(user is None):
            raise ValueError("Usuário não cadastrado")
        
        if(user.user_type_id == 3):
            raise ValueError("Usuário não é motorista")
                
        if(self.vehicle_type_service.get_type(vehicle.vehicle_type_id) is None):
            raise ValueError("Tipo de veículo inválido")
        
        return user

    def validating_vehicle_update(self, vehicle: UpdateVehicle):
        if(self.vehicle_repository.get_vehicle(vehicle.id) is None):
            raise ValueError("Veículo não encontrado")

        if(len(vehicle.plate) != 7):
            raise ValueError("Placa incorreta")
        
        vehicle_db = self.vehicle_repository.get_vehicle_by_plate(vehicle.plate)

        if(vehicle_db is not None and vehicle.id != vehicle_db.id):
            raise ValueError("Veículo já registrado")

        user = self.user_service.get_user(vehicle.user_id)

        if(user is None):
            raise ValueError("Usuário não cadastrado")
        
        if(user.user_type_id == 3):
            raise ValueError("Usuário não é motorista")
        
        return user
                
    def validating_vehicle_delete(self, vehicle_id: int):
        vehicle = self.vehicle_repository.get_vehicle(vehicle_id)
        if(vehicle is None):
            raise ValueError("Veículo não encontrado")
        
        return vehicle
        
    def validating_vehicle_by_driver(self, user_id: int):
        user = self.user_service.get_user(user_id)

        if(user is None):
            raise ValueError("Usuário não cadastrado")
        
        if(user.user_type_id != 2 and user.user_type_id != 1):
            raise ValueError("Usuário não é motorista")
        
    def creating_driver_code(self, driver: UserModel, vehicle: CreateVehicle):
        code = self.generate_driver_code(vehicle.plate, driver.name.upper())

        return code

    def generate_driver_code(self, plate: str, name: str):
        initials = "".join([separate_name[0].upper() for separate_name in name.split()])

        if(len(initials) > 1):
            return f"{initials[0]}{initials[1]}{plate}"
        
        return f"{name[0]}{name[1]}{plate}"