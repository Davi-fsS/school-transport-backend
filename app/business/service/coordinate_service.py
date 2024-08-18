from data.model.coordinate_model import CoordinateModel
from business.service.user_service import UserService
from data.repository.coordinate_repository import CoordinateRepository
from presentation.dto import SaveCoordinate
from datetime import datetime

class PointService():
    coordinate_repository: CoordinateRepository
    user_service: UserService

    def __init__(self):
        self.coordinate_repository = CoordinateRepository()
        self.user_service = UserService()

    def save_coordinates_mobile(self, coordinate: SaveCoordinate):
        if(coordinate.lat is None):
            raise ValueError("Coordenada inválida")
        
        if(coordinate.lng is None):
            raise ValueError("Coordenada inválida")
        
        if(coordinate.user_id is None):
            raise ValueError("Usuário inválido")
        
        user = self.user_service.get_user(coordinate.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário inválido")    

        coordinate_db = CoordinateModel(lat=coordinate.lat, lng=coordinate.lng, alt=coordinate.alt,
                                        coordinate_type_id=1, register_data=datetime.now(),
                                        schedule_id=1)
        
        self.coordinate_repository.save_coordinates(coordinate_db)


