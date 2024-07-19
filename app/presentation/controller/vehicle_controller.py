from business.service.vehicle_service import VehicleService
from presentation.dto.CreateVehicle import CreateVehicle
from presentation.dto.UpdateVehicle import UpdateVehicle

class VehicleController():
    vehicle_service: VehicleService

    def __init__(self):
        self.vehicle_service = VehicleService()
    
    def create_vehicle(self, vehicle: CreateVehicle):
        return self.vehicle_service.create_vehicle(vehicle)
    
    def update_vehicle(self, vehicle: UpdateVehicle):
        return self.vehicle_service.update_vehicle(vehicle)
    
    def delete_vehicle(self, vehicle_id: int):
        return self.vehicle_service.delete_vehicle(vehicle_id)