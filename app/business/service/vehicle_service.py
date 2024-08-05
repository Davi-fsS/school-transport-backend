from data.repository.vehicle_repository import VehicleRepository
from business.service.user_service import UserService
from business.service.vehicle_type_service import VehicleTypeService
from data.model.vehicle_model import VehicleModel
from presentation.dto.CreateVehicle import CreateVehicle
from presentation.dto.UpdateVehicle import UpdateVehicle

class VehicleService():
    vehicle_repository: VehicleRepository
    user_service: UserService
    vehicle_type_service: VehicleTypeService

    def __init__(self):
        self.vehicle_repository = VehicleRepository()
        self.user_service = UserService()
        self.vehicle_type_service = VehicleTypeService()

    def create_vehicle(self, vehicle: CreateVehicle):
        self.validating_vehicle_create(vehicle)

        vehicle_model = VehicleModel(plate=vehicle.plate, 
                                     vehicle_type_id=vehicle.vehicle_type_id,
                                     user_id=vehicle.user_id,
                                     creation_user = 2
                                    )

        return self.vehicle_repository.create_vehicle(vehicle_model)
    
    def update_vehicle(self, vehicle: UpdateVehicle):
        self.validating_vehicle_update(vehicle)

        return self.vehicle_repository.update_vehicle(vehicle)

    def delete_vehicle(self, vehicle_id: int):
        self.validating_vehicle_delete(vehicle_id)

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
        
        if(user.user_type_id != 2):
            raise ValueError("Usuário não é motorista")
        
        if(self.vehicle_repository.get_vehicle_by_driver(vehicle.user_id) is not None):
            raise ValueError("Motorista já possuí veículo")
        
        if(self.vehicle_type_service.get_type(vehicle.vehicle_type_id) is None):
            raise ValueError("Tipo de veículo inválido")
        
    def validating_vehicle_update(self, vehicle: UpdateVehicle):
        if(self.vehicle_repository.get_vehicle(vehicle.id) is None):
            raise ValueError("Veículo não encontrado")

        if(len(vehicle.plate) != 7):
            raise ValueError("Placa incorreta")
        
        vehicle_db = self.vehicle_repository.get_vehicle_by_plate(vehicle.plate)

        if(vehicle.id != vehicle_db.id and vehicle_db is not None):
            raise ValueError("Veículo já registrado")

        user = self.user_service.get_user(vehicle.user_id)

        if(user is None):
            raise ValueError("Usuário não cadastrado")
        
        if(user.user_type_id != 2):
            raise ValueError("Usuário não é motorista")
                
    def validating_vehicle_delete(self, vehicle_id: int):
        if(self.vehicle_repository.get_vehicle(vehicle_id) is None):
            raise ValueError("Veículo não encontrado")
        
    def validating_vehicle_by_driver(self, user_id: int):
        user = self.user_service.get_user(user_id)

        if(user is None):
            raise ValueError("Usuário não cadastrado")
        
        if(user.user_type_id != 2):
            raise ValueError("Usuário não é motorista")