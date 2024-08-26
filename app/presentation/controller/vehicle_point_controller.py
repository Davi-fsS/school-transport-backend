from business.service.vehicle_point_service import VehiclePointService

class VehiclePointController():
    vehicle_point_service: VehiclePointService

    def __init__(self):
        self.vehicle_point_service = VehiclePointService()
    
    def get_vehicle_point_association(self, vehicle_id: int, point_id: int):
        return self.vehicle_point_service.get_vehicle_point_association(vehicle_id, point_id)
    
    def get_association_by_user(self, user_id: int):
        return self.vehicle_point_service.get_association_by_user(user_id)