from presentation.dto.VehiclePointAssociation import VehiclePointAssociation
from business.service.vehicle_service import VehicleService
from presentation.dto.CreateVehicle import CreateVehicle
from presentation.dto.UpdateVehicle import UpdateVehicle

class VehicleController():
    vehicle_service: VehicleService

    def __init__(self):
        self.vehicle_service = VehicleService()
    
    def get_all_vehicle(self):
        return self.vehicle_service.get_all_vehicle()

    def create_vehicle(self, vehicle: CreateVehicle):
        return self.vehicle_service.create_vehicle(vehicle)
    
    def update_vehicle(self, vehicle: UpdateVehicle):
        return self.vehicle_service.update_vehicle(vehicle)
    
    def vehicle_association_point(self, association: VehiclePointAssociation):
        return self.vehicle_service.vehicle_association_point(association)
    
    def vehicle_disassociation_point(self,disassociation: VehiclePointAssociation):
        return self.vehicle_service.vehicle_disassociation_point(disassociation)
    
    def delete_vehicle(self, vehicle_id: int):
        return self.vehicle_service.delete_vehicle(vehicle_id)
    
    def get_vehicle_by_driver(self, user_id: int):
        return self.vehicle_service.get_vehicle_by_driver(user_id)