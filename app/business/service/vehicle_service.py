from data.repository.vehicle_repository import VehicleRepository
from data.model.vehicle_model import VehicleModel

class VehicleService():
    vehicle_repository: VehicleRepository

    def __init__(self):
        self.vehicle_repository = VehicleRepository()

    def create_vehicle(self, vehicle: VehicleModel):
        return self.vehicle_repository.create_vehicle(vehicle)
