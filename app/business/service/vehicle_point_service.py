from presentation.dto.User import User
from business.service.user_service import UserService
from data.repository.vehicle_point_repository import VehiclePointRepository

class VehiclePointService():
    vehicle_point_repository: VehiclePointRepository
    user_service: UserService

    def __init__(self):
        self.vehicle_point_repository = VehiclePointRepository()
        self.user_service = UserService()

    def get_vehicle_point_association(self, vehicle_id: int, point_id: int):
        return self.vehicle_point_repository.get_vehicle_point_association(vehicle_id, point_id)