from data.model.coordinate_model import CoordinateModel
from business.service.user_service import UserService
from data.repository.coordinate_repository import CoordinateRepository
from presentation.dto.SaveCoordinate import SaveCoordinate
from datetime import datetime

class CoordinateService():
    coordinate_repository: CoordinateRepository
    user_service: UserService

    def __init__(self):
        self.coordinate_repository = CoordinateRepository()
        self.user_service = UserService()

    def save_coordinates_mobile(self, coordinate: SaveCoordinate):
        user = self.user_service.get_user(coordinate.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário inválido")    
        
        coordinate_db = CoordinateModel(lat=coordinate.lat, lng=coordinate.lng, coordinate_type_id=1, 
                                        register_date=datetime.now(), creation_user=coordinate.user_id, schedule_id=1)
        
        return self.coordinate_repository.save_coordinates(coordinate_db)


