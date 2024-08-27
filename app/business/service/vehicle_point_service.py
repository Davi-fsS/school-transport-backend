from typing import List
from presentation.dto.UpdateVehiclePoint import UpdateVehiclePoint
from data.model.vehicle_point_model import VehiclePointModel
from presentation.dto.CreateVehiclePoint import CreateVehiclePoint
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
                    
    def create_vehicle_point(self, vehicle_point: CreateVehiclePoint):
        user = self.user_service.get_user(vehicle_point.user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        vehicle = self.vehicle_service.get_vehicle_by_id(vehicle_point.vehicle_id)

        if vehicle is None:
            raise ValueError("Veículo não existe")

        vehicles = self.vehicle_service.get_vehicle_list_by_driver(user.id)

        if len(vehicles) == 0:
            raise ValueError("Nenhum veículo associado ao motorista")
        
        vehicle_id_list = []
        for vehicle in vehicles:
            vehicle_id_list.append(vehicle.id)
        
        if vehicle_point.vehicle_id not in vehicle_id_list:
            raise ValueError("Veículo não pertence a este motorista")
        
        point = self.point_service.get_point_by_id(vehicle_point.point_id)

        if point is None:
            raise ValueError("Ponto não existe")
        
        if point.point_type_id == 1:
            raise ValueError("Ponto não é uma escola")
        
        points = self.point_service.get_school_by_driver(user.id)

        if len(points) == 0:
            raise ValueError("Nenhum ponto associado ao motorista")
        
        point_id_list = []
        for point in points:
            point_id_list.append(point.id)

        if vehicle_point.point_id not in point_id_list:
            raise ValueError("Escola não pertence a este motorista")
        
        vehicle_point_with_these_combination = self.vehicle_point_repository.get_vehicle_point_association(vehicle_point.vehicle_id, point_id=vehicle_point.point_id)

        if vehicle_point_with_these_combination is not None:
            raise ValueError("Associação já existe")
        
        vehicle_point_code = self.generate_code(user.name, vehicle.plate, point.name)
        
        vehicle_point_create = VehiclePointModel(vehicle_id=vehicle_point.vehicle_id,
                                                 point_id=vehicle_point.point_id,
                                                 creation_user=user.id,
                                                 code=vehicle_point_code)

        return self.vehicle_point_repository.create_vehicle_point(vehicle_point_create)
    
    def update_vehicle_point(self, update_body: UpdateVehiclePoint):
        vehicle_point = self.vehicle_point_repository.get_vehicle_point_by_id(update_body.vehicle_point_id)

        if vehicle_point is None:
            raise ValueError("Associação não existe")
        
        if vehicle_point.vehicle_id == update_body.vehicle_id and vehicle_point.point_id == update_body.point_id:
            raise ValueError("Associação já existe")

        user = self.user_service.get_user(update_body.user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        vehicle_body = self.vehicle_service.get_vehicle_by_id(update_body.vehicle_id)

        if vehicle_body is None:
            raise ValueError("Veículo não existe")

        vehicles = self.vehicle_service.get_vehicle_list_by_driver(user.id)

        if len(vehicles) == 0:
            raise ValueError("Nenhum veículo associado ao motorista")
        
        vehicle_id_list = []
        for vehicle in vehicles:
            vehicle_id_list.append(vehicle.id)
        
        if update_body.vehicle_id not in vehicle_id_list:
            raise ValueError("Veículo não pertence a este motorista")
        
        point_body = self.point_service.get_point_by_id(update_body.point_id)

        if point_body is None:
            raise ValueError("Ponto não existe")
        
        if point_body.point_type_id == 1:
            raise ValueError("Ponto não é uma escola")
        
        points = self.point_service.get_school_by_driver(user.id)

        if len(points) == 0:
            raise ValueError("Nenhum ponto associado ao motorista")
        
        point_id_list = []
        for point in points:
            point_id_list.append(point.id)

        if update_body.point_id not in point_id_list:
            raise ValueError("Escola não pertence a este motorista")
        
        vehicle_point_with_these_combination = self.vehicle_point_repository.get_vehicle_point_association(update_body.vehicle_id, point_id=update_body.point_id)

        if vehicle_point_with_these_combination is not None:
            raise ValueError("Associação já existe")
                
        vehicle_point_code = self.generate_code(user.name, vehicle_body.plate, point_body.name)

        return self.vehicle_point_repository.update_vehicle_point(update_body, vehicle_point_code)

    def delete_vehicle_point(self, vehicle_point_id: int):
        self.vehicle_point_repository.delete_vehicle_point(vehicle_point_id)

    def generate_code(self, user_name: str, vehicle_plate: str, school_name: str):
        name = ''.join([palavra[0] for palavra in user_name.split()])
        school = ''.join([palavra[0] for palavra in school_name.split()]) 
        return f"{name[:2]}{vehicle_plate[:2]}{school}{vehicle_plate[-2:]}".upper()