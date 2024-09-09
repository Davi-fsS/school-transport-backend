from presentation.dto.Vehicle import Vehicle
from presentation.dto.VehiclePoint import VehiclePoint
from data.repository.user_repository import UserRepository
from data.repository.vehicle_repository import VehicleRepository
from data.repository.point_repository import PointRepository
from business.service.user_point_service import UserPointService
from presentation.dto.CreatePoint import CreatePoint
from presentation.dto.DriverAssociation import DriverAssociation
from presentation.dto.UpdatePoint import UpdatePoint
from presentation.dto.SchoolAssociation import SchoolAssociation
from presentation.dto.Point import Point
from data.model.point_model import PointModel
from business.external_service.google_geocoding_service import GoogleGeocodingService
from typing import List

class PointService():
    point_repository: PointRepository
    google_geocoding_service: GoogleGeocodingService
    user_point_service: UserPointService
    vehicle_repository: VehicleRepository
    user_repository: UserRepository

    def __init__(self):
        self.point_repository = PointRepository()
        self.google_geocoding_service = GoogleGeocodingService()
        self.user_point_service = UserPointService()
        self.vehicle_repository = VehicleRepository()
        self.user_repository = UserRepository()

    def get_point_by_id(self, point_id : int):
        return self.point_repository.get_point(point_id)
    
    def get_school_by_id(self, point_id : int):
        return self.point_repository.get_school(point_id)
    
    def get_school_by_user(self, user_id : int):
        user_points = self.user_point_service.get_user_point_list(user_id)

        point_id_list = []
        for user_point in user_points:
            point_id_list.append(user_point.point_id)

        return self.point_repository.get_first_point_school_by_point_list(point_id_list)
    
    def get_school_associated_by_driver(self, user_id : int):
        vehicle_point_list_dto: List[VehiclePoint] = []

        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário não existe")

        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        vehicles = self.vehicle_repository.get_vehicle_list_by_driver(user.id)

        points = self.point_repository.get_all_school_list()

        for vehicle in vehicles:
            for point in points:
                if(point.id == vehicle.point_id):
                    point_dto = Point(id=point.id, name=point.name, address=point.address, lat=point.lat, lng=point.lng,
                                      city=point.city, neighborhood=point.neighborhood, state=point.state, description=point.description,
                                      alt=point.alt,point_type_id=point.point_type_id)
                    
                    vehicle_dto = Vehicle(id=vehicle.id, plate=vehicle.plate, vehicle_type_id=vehicle.vehicle_type_id,
                                        color=vehicle.color, model=vehicle.model, year=vehicle.year, code=vehicle.code)

                    vehicle_point_list_dto.append(VehiclePoint(vehicle=vehicle_dto, school=point_dto))

        return vehicle_point_list_dto
    
    def get_school_by_driver(self, user_id : int):
        school_association: List[SchoolAssociation] = []

        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário não existe")

        if user.user_type_id == 3:
            raise ValueError("Usuário não é um motorista")
        
        user_points = self.user_point_service.get_user_point_list(user.id)

        point_id_list = []
        for user_point in user_points:
            point_id = user_point.point_id
            point_id_list.append(point_id)

        points = self.point_repository.get_points_school_by_point_list(point_id_list)

        for point in points:
            for user_point in user_points:
                if(user_point.point_id == point.id):
                    point_dto = Point(id=point.id, name=point.name, address=point.address, lat=point.lat,
                                      lng=point.lng, alt=point.alt, city=point.city, neighborhood=point.neighborhood,
                                      state=point.state, description=point.description, point_type_id=point.point_type_id)
                    school = SchoolAssociation(point=point_dto, code=user_point.code)
                    school_association.append(school)

        return school_association
    
    def get_points_by_user_list(self, user_list: List[int]):
        user_points = self.user_point_service.get_user_point_list_by_user_list(user_list)

        point_id_list = []
        for user_point in user_points:
            point_id_list.append(user_point.point_id)
        
        return self.point_repository.get_points_home_by_point_list(point_id_list)
    
    def get_point_user_id(self, user_id : int):
        user_points = self.user_point_service.get_user_point_list(user_id)

        point_id_list = []
        for user_point in user_points:
            point_id_list.append(user_point.point_id)

        return self.point_repository.get_points_home_by_point_list(point_id_list)

    def create_point(self, point: CreatePoint):
        coords = self.google_geocoding_service.get_geocode_by_address(point.address, point.city)

        point_body = {}

        if(point.point_type_id == 1):
            point_body = PointModel(name=f"Casa {point.name}", city=point.city, neighborhood=point.neighborhood, state=point.state, address=point.address, point_type_id=point.point_type_id, lat=coords["lat"], lng= coords["lng"] ,description=f"Endereço principal de {point.name}", creation_user=2)
        else:
            point_body = PointModel(name=point.name, city=point.city, neighborhood=point.neighborhood, state=point.state, address=point.address, point_type_id=point.point_type_id, lat=coords["lat"], lng= coords["lng"] ,description=point.description, creation_user=2)

        return self.point_repository.create_point(point_body)
    
    def create_driver_point_association(self, association: DriverAssociation):
        code = self.validate_driver_point_association(association)

        self.user_point_service.create_user_point(association.user_id, association.point_id, True, code=code)
    
    def delete_driver_point_association(self, disassociation: DriverAssociation):
        self.validate_driver_point_disassociation(disassociation)

        self.user_point_service.delete_user_point(disassociation.user_id, disassociation.point_id)
    
    def validate_driver_point_disassociation(self, disassociation: DriverAssociation):
        point = self.point_repository.get_point(disassociation.point_id)

        if(point.point_type_id != 2):
            raise ValueError("Este ponto não é uma escola")

    def validate_driver_point_association(self, association: DriverAssociation):
        user = self.user_repository.get_user(association.user_id)

        if(user is None):
            raise ValueError("Usuário não identificado")
        
        point_db = self.point_repository.get_point(association.point_id)

        if(point_db.point_type_id != 2):
            raise ValueError("Este ponto não é uma escola")

        points_by_user = self.user_point_service.get_user_point_list(association.user_id)

        points_ids_by_user = []

        for point in points_by_user:
            point_id = point.id
            points_ids_by_user.append(point_id)

        driver_with_school = self.point_repository.get_points_school_by_point_list(points_ids_by_user)

        if(len(driver_with_school) != 0):
            raise ValueError("Já existe uma escola associada ao seu usuário")
        
        code = self.generate_code(user.name, point_db.name)

        return code

    def update_point(self, point: UpdatePoint):
        self.validating_point_update(point)

        coords = self.google_geocoding_service.get_geocode_by_address(point.address, point.city)

        return self.point_repository.update_point(lat=coords["lat"], lng= coords["lng"], point_update=point)
    
    def get_point(self, point_id: int):
        return self.point_repository.get_point(point_id=point_id)
    
    def get_point_home_by_user_id(self, user_id: int):
        user_points = self.user_point_service.get_user_point_list(user_id)

        if(len(user_points) > 0):
            point_id_list = []
            for user_point in user_points:
                point_id_list.append(user_point.point_id)

            points = self.get_point_home_list_by_user(point_id_list)

            return points[0]
        else:
            raise ValueError("Responsável sem endereço registrado")

    def get_point_list_by_user(self, point_list: List[int]):
        points_list = self.point_repository.get_points_by_point_list(point_list)

        points_list_dto = []
        for point in points_list:
            point_dto = Point(id=point.id, name=point.name, address=point.address, lat=point.lat, lng=point.lng, alt=point.alt, city=point.city, neighborhood=point.neighborhood, state=point.state, description=point.description, point_type_id=point.point_type_id)
            points_list_dto.append(point_dto)

        return points_list_dto
    
    def get_point_home_list_by_user(self, point_list: List[int]):
        points_list = self.point_repository.get_points_home_by_point_list(point_list)

        points_list_dto = []
        for point in points_list:
            point_dto = Point(id=point.id, name=point.name, address=point.address, lat=point.lat, lng=point.lng, alt=point.alt, city=point.city, neighborhood=point.neighborhood, state=point.state, description=point.description, point_type_id=point.point_type_id)
            points_list_dto.append(point_dto)

        return points_list_dto

    def get_point_school_list_by_user(self, point_list: List[int]):
        point = self.point_repository.get_first_point_school_by_point_list(point_list)

        point_dto = Point(id=point.id, name=point.name, address=point.address,
                          lat=point.lat, lng=point.lng, city=point.city, description=point.description,
                          neighborhood=point.neighborhood, state=point.state, point_type_id=point.point_type_id)

        return point_dto


    def get_all_school_list(self):
        return self.point_repository.get_all_school_list()
    
    def delete_point(self, point_id: int):
        self.validating_point_delete(point_id)

        self.user_point_service.delete_user_point_list_by_point(point_id)

        return self.point_repository.delete_point(point_id)
        
    def validating_point_delete(self, school_id: int):
        if(self.point_repository.get_school(school_id) is None):
            raise ValueError("Ponto inválido")
        
    def validating_point_update(self, point: UpdatePoint):
        if(self.point_repository.get_point(point.id) is None):
            raise ValueError("Ponto inválido")
    
    def generate_code(self, user_name: str, school_name: str):
        name = ''.join([palavra[0] for palavra in user_name.split()])
        school = ''.join([palavra[0] for palavra in school_name.split()]) 
        return f"{name[:2]}{school}".upper()