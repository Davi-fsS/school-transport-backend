from data.repository.point_repository import PointRepository
from presentation.dto.CreatePoint import CreatePoint
from data.model.point_model import PointModel
from business.external_service.google_geocoding_service import GoogleGeocodingService

class PointService():
    point_repository: PointRepository
    google_geocoding_service: GoogleGeocodingService

    def __init__(self):
        self.point_repository = PointRepository()
        self.google_geocoding_service = GoogleGeocodingService()

    def create_point(self, point_name: str, point: CreatePoint):
        coords = self.google_geocoding_service.get_geocode_by_address(point.address)

        point_body = PointModel(name=f"Casa {point_name}", address=point.address, point_type_id=1, lat=coords["lat"], lng= coords["lng"] ,description=f"Endereço principal de {point_name}", creation_user=2)

        return self.point_repository.create_point(point_body)
