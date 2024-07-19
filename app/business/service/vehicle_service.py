from data.repository.vehicle_repository import VehicleRepository
from business.service.user_service import UserService
from data.model.vehicle_model import VehicleModel
from presentation.dto.CreateVehicle import CreateVehicle
from presentation.dto.UpdateVehicle import UpdateVehicle

class VehicleService():
    vehicle_repository: VehicleRepository
    user_service: UserService

    def __init__(self):
        self.vehicle_repository = VehicleRepository()
        self.user_service = UserService()

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
        
    def validating_vehicle_update(self, vehicle: UpdateVehicle):
        if(self.vehicle_repository.get_vehicle(vehicle.id) is None):
            raise ValueError("Veículo não encontrado")

        if(len(vehicle.plate) != 7):
            raise ValueError("Placa incorreta")
        
        if(self.vehicle_repository.get_vehicle_by_plate(vehicle.plate) is not None):
            raise ValueError("Veículo já registrado")
        
        user = self.user_service.get_user(vehicle.user_id)

        if(user is None):
            raise ValueError("Usuário não cadastrado")
        
        if(user.user_type_id != 2):
            raise ValueError("Usuário não é motorista")