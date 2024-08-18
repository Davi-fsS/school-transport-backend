from presentation.dto import SaveCoordinate
from business.service.coordinate_service import CoordinateService

class CoordinateController():
    coordinate_service : CoordinateService

    def __init__(self):
        self.coordinate_service = CoordinateService()

    def save_coordinate_mobile(self, coordinates: SaveCoordinate):
        return self.coordinate_service.save_coordinates_mobile(coordinates)