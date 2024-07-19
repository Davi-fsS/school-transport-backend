from data.repository.vehicle_repository import VehicleRepository
from data.model.vehicle_model import VehicleModel
from presentation.dto.CreateVehicle import CreateVehicle

class VehicleService():
    vehicle_repository: VehicleRepository

    def __init__(self):
        self.vehicle_repository = VehicleRepository()

    def create_vehicle(self, vehicle: CreateVehicle):
        vehicle_model = VehicleModel(plate=vehicle.plate, 
                                     vehicle_type_id=vehicle.vehicle_type_id,
                                     color=vehicle.color,
                                     model=vehicle.model,
                                     year=vehicle.year,
                                     chassi=vehicle.chassi,
                                     renavam=vehicle.renavam,
                                     user_id=vehicle.user_id,
                                     creation_user = 2
                                    )

        return self.vehicle_repository.create_vehicle(vehicle_model)
