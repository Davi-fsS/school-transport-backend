from business.service.vehicle_service import VehicleService
from presentation.dto.CreateVehicle import CreateVehicle

class VehicleController():
    vehicle_service: VehicleService

    def __init__(self):
        self.vehicle_service = VehicleService()
    
    def create_vehicle(self, vehicle: CreateVehicle):
        return self.vehicle_service.create_vehicle(vehicle)