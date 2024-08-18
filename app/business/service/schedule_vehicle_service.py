from business.service.user_service import UserService
from presentation.dto.Vehicle import Vehicle
from business.service.vehicle_service import VehicleService
from data.repository.schedule_vehicle_repository import ScheduleVehicleRepository

class ScheduleVehicleService():
    schedule_vehicle_repository: ScheduleVehicleRepository
    vehicle_service: VehicleService
    user_service: UserService

    def __init__(self):
        self.schedule_vehicle_repository = ScheduleVehicleRepository()
        self.vehicle_service = VehicleService()
        self.user_service = UserService()

    def get_schedule_user_by_schedule_id(self, schedule_id: int):
        return self.schedule_vehicle_repository.get_schedule_vehicle_by_schedule_id(schedule_id)
    
    def get_vehicle_by_schedule_id(self, schedule_id: int):
        schedule_vehicle = self.schedule_vehicle_repository.get_schedule_vehicle_by_schedule_id(schedule_id)

        if(schedule_vehicle is None):
            raise ValueError("Não existe usuário associado a esta viagem")
        
        vehicle = self.vehicle_service.get_vehicle_by_id(schedule_vehicle.vehicle_id)

        if(vehicle is None):
            raise ValueError("Veículo inválido")
        
        user_with_vehicle = self.user_service.get_user(vehicle.user_id)

        if(user_with_vehicle.user_type_id == 3):
            raise ValueError("Responsável não deve ter carro associado")

        vehicle_dto = Vehicle(id=vehicle.id, plate=vehicle.plate, color=vehicle.color,
                           vehicle_type_id=vehicle.vehicle_type_id, model=vehicle.model,
                           year=vehicle.year)
        
        return vehicle_dto