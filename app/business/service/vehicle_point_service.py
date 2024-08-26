from typing import List
from presentation.dto.Vehicle import Vehicle
from presentation.dto.Point import Point
from presentation.dto.PointVehicle import PointVehicle
from business.service.point_service import PointService
from business.service.user_service import UserService
from business.service.vehicle_service import VehicleService
from data.repository.vehicle_point_repository import VehiclePointRepository

class VehiclePointService():
    vehicle_point_repository: VehiclePointRepository
    user_service: UserService
    vehicle_service: VehicleService
    point_service: PointService

    def __init__(self):
        self.vehicle_point_repository = VehiclePointRepository()
        self.user_service = UserService()
        self.vehicle_service = VehicleService()
        self.point_service = PointService()

    def get_vehicle_point_association(self, vehicle_id: int, point_id: int):
        return self.vehicle_point_repository.get_vehicle_point_association(vehicle_id, point_id)
    
    def get_association_by_user(self, user_id: int):
        point_vehicles_list : List[PointVehicle] = []

        user = self.user_service.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")

        vehicles = self.vehicle_service.get_vehicle_list_by_driver(user.id)

        if len(vehicles) == 0:
            raise ValueError("Nenhum veículo associado ao motorista")
        
        vehicle_id_list = []
        for vehicle in vehicles:
            vehicle_id_list.append(vehicle.id)
        
        points = self.point_service.get_school_by_driver(user.id)

        if len(points) == 0:
            raise ValueError("Nenhum ponto associado ao motorista")
        
        point_id_list = []
        for point in points:
            point_id_list.append(point.id)
        
        point_vehicles = self.vehicle_point_repository.get_vehicle_point_association_by_vehicle_list(vehicle_id_list)

        for point_vehicle in point_vehicles:
            point_vehicle_dto = PointVehicle(id=point_vehicle.id, code=point_vehicle.code)
            for point in points:
                if(point.id == point_vehicle.point_id):
                    point_vehicle_dto.point = Point(id=point.id, name=point.name, address=point.address, lat=point.lat, lng=point.lng, alt=point.alt,
                                      city=point.city, neighborhood=point.neighborhood, state=point.state, description=point.description,
                                      point_type_id=point.point_type_id)
            for vehicle in vehicles:
                if(vehicle.id == point_vehicle.vehicle_id):
                    point_vehicle_dto.vehicle = Vehicle(id=vehicle.id, plate=vehicle.plate, vehicle_type_id=vehicle.vehicle_type_id,
                                                        color=vehicle.color, model=vehicle.model, year=vehicle.year, code=vehicle.code)
            
            point_vehicles_list.append(point_vehicle_dto)

        return point_vehicles_list
                    
