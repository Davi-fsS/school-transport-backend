from business.service.vehicle_service import VehicleService
from data.model.vehicle_model import VehicleModel

class VehicleController():
    vehicle_service: VehicleService

    def __init__(self):
        self.vehicle_service = VehicleService()
    
    def create_vehicle(self, vehicle: VehicleModel):
        return self.vehicle_service.create_vehicle(vehicle)