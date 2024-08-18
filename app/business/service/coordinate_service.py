from presentation.dto.Coordinate import Coordinate
from presentation.dto.CoordinateInSchedule import CoordinateInSchedule
from business.service.schedule_service import ScheduleService
from data.model.coordinate_model import CoordinateModel
from business.service.user_service import UserService
from data.repository.coordinate_repository import CoordinateRepository
from presentation.dto.SaveCoordinate import SaveCoordinate
from datetime import datetime

class CoordinateService():
    coordinate_repository: CoordinateRepository
    schedule_service: ScheduleService
    user_service: UserService

    def __init__(self):
        self.coordinate_repository = CoordinateRepository()
        self.user_service = UserService()
        self.schedule_service = ScheduleService()

    def save_coordinates_mobile(self, coordinate: SaveCoordinate):
        user = self.user_service.get_user(coordinate.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário inválido")    
        
        coordinate_db = CoordinateModel(lat=coordinate.lat, lng=coordinate.lng, coordinate_type_id=1, 
                                        register_date=datetime.now(), creation_user=coordinate.user_id, schedule_id=1)
        
        return self.coordinate_repository.save_coordinates(coordinate_db)
    
    def get_coordinates_by_schedule(self, schedule_id: int):
        schedule = self.schedule_service.get_schedule_by_id(schedule_id)

        if(schedule is None):
            raise ValueError("Viagem não encontrada")
        
        coordinates_by_schedule_id = self.coordinate_repository.get_list_coordinates_by_schedule_id(schedule_id)

        list_coordinates_dto  = []

        for coord in coordinates_by_schedule_id:
            coordinate_dto = Coordinate(lat=coord.lat, lng=coord.lng, schedule_id=coord.schedule_id,
                                        coordinate_type_id=coord.coordinate_type_id, register_date=coord.register_date,
                                        creation_user=coord.creation_user)
            list_coordinates_dto.append(coordinate_dto)

        coordinate_dto = CoordinateInSchedule(schedule=schedule, coordinates=list_coordinates_dto)

        return coordinate_dto