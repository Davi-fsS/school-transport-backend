from presentation.dto.SaveLoraCoordinate import SaveLoraCoordinate
from presentation.dto.SaveCoordinate import SaveCoordinate
from business.service.coordinate_service import CoordinateService

class CoordinateController():
    coordinate_service : CoordinateService

    def __init__(self):
        self.coordinate_service = CoordinateService()

    def save_coordinate_mobile(self, coordinates: SaveCoordinate):
        return self.coordinate_service.save_coordinates_mobile(coordinates)
    
    def save_coordinate_lora(self, coordinates: SaveLoraCoordinate):
        return self.coordinate_service.save_coordinate_lora(coordinates)
    
    def get_coordinates_by_schedule(self, schedule_id: int):
        return self.coordinate_service.get_coordinates_by_schedule(schedule_id)
    
    def get_last_coordinate_by_schedule(self, schedule_id: int, user_id: int):
        return self.coordinate_service.get_last_coordinate_by_schedule(schedule_id, user_id)