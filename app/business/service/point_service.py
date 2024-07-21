from data.repository.point_repository import PointRepository
from presentation.dto.CreatePoint import CreatePoint
from presentation.dto.CreateSchool import CreateSchool
from presentation.dto.UpdateSchool import UpdateSchool
from presentation.dto.UpdatePoint import UpdatePoint
from data.model.point_model import PointModel
from business.external_service.google_geocoding_service import GoogleGeocodingService

class PointService():
    point_repository: PointRepository
    google_geocoding_service: GoogleGeocodingService

    def __init__(self):
        self.point_repository = PointRepository()
        self.google_geocoding_service = GoogleGeocodingService()

    def create_point(self, point_name: str, point: CreatePoint):
        coords = self.google_geocoding_service.get_geocode_by_address(point.address, point.city)

        point_body = PointModel(name=f"Casa {point_name}", city=point.city, neighborhood=point.neighborhood, state=point.state, address=point.address, point_type_id=1, lat=coords["lat"], lng= coords["lng"] ,description=f"Endereço principal de {point_name}", creation_user=2)

        return self.point_repository.create_point(point_body)
    
    def update_point(self, point: UpdatePoint):
        self.validating_point_update(point)

        coords = self.google_geocoding_service.get_geocode_by_address(point.address, point.city)

        return self.point_repository.update_point(lat=coords["lat"], lng= coords["lng"], point_update=point)
    
    def get_point(self, point_id: int):
        return self.point_repository.get_point(point_id=point_id)
    
    def get_all_school_list(self):
        return self.point_repository.get_all_school_list()

    def create_school(self, school: CreateSchool):
        coords = self.google_geocoding_service.get_geocode_by_address(school.address, school.city)

        point_body = PointModel(name=school.name, city=school.city, neighborhood=school.neighborhood, state=school.state, address=school.address, point_type_id=2, lat=coords["lat"], lng= coords["lng"] ,description=school.description, creation_user=2)

        return self.point_repository.create_point(point_body)
    
    def update_school(self, school: UpdateSchool):
        self.validating_school_update(school)

        coords = self.google_geocoding_service.get_geocode_by_address(school.address, school.city)

        return self.point_repository.update_school(lat=coords["lat"], lng= coords["lng"], school_update=school)
    
    def delete_school(self, school_id: int):
        self.validating_school_delete(school_id)

        return self.point_repository.delete_school(school_id)
    
    def validating_school_update(self, school: UpdateSchool):
        if(self.point_repository.get_school(school_id=school.id) is None):
            raise ValueError("Ponto inválido")
        
    def validating_school_delete(self, school_id: int):
        if(self.point_repository.get_school(school_id) is None):
            raise ValueError("Ponto inválido")
        
    def validating_point_update(self, point: UpdatePoint):
        if(self.point_repository.get_point(point.id) is None):
            raise ValueError("Ponto inválido")