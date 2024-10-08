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

        schedule = self.schedule_service.get_schedule_in_progress(coordinate.schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")
        
        coordinate_db = CoordinateModel(lat=coordinate.lat, lng=coordinate.lng, coordinate_type_id=1, 
                                        register_date=datetime.now(), creation_user=coordinate.user_id, schedule_id=coordinate.schedule_id)
        
        return self.coordinate_repository.save_coordinates(coordinate_db)
    
    def get_coordinates_by_schedule(self, schedule_id: int):
        schedule = self.schedule_service.get_schedule_by_id(schedule_id)
        
        coordinates_by_schedule_id = self.coordinate_repository.get_list_coordinates_by_schedule_id(schedule_id)

        list_coordinates_dto  = []

        for coord in coordinates_by_schedule_id:
            coordinate_dto = Coordinate(lat=coord.lat, lng=coord.lng, schedule_id=coord.schedule_id,
                                        coordinate_type_id=coord.coordinate_type_id, register_date=coord.register_date,
                                        creation_user=coord.creation_user)
            list_coordinates_dto.append(coordinate_dto)

        coordinate_dto = CoordinateInSchedule(schedule=schedule, coordinates=list_coordinates_dto)

        return coordinate_dto
    
    def get_last_coordinate_by_schedule(self, schedule_id: int, user_id: int):
        user = self.user_service.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        schedule = self.schedule_service.get_schedule_by_id(schedule_id)

        if schedule is None:
            raise ValueError("Viagem inválida")
        responsibles_in_schedule = self.schedule_service.get_responsibles_in_schedule(schedule_id)

        responsible_id_list = []

        for responsible in responsibles_in_schedule:
            responsible_id_list.append(responsible.id)

        if user.id not in responsible_id_list:
            raise ValueError("Usuário não permitido")

        last_coord = self.coordinate_repository.get_last_coordinate_by_schedule_id(schedule_id)    

        if last_coord is None:
            raise ValueError("Não possui nenhuma coordenada para essa viagem")

        return Coordinate(lat=last_coord.lat, lng=last_coord.lng, schedule_id=last_coord.schedule_id,
                            coordinate_type_id=last_coord.coordinate_type_id, register_date=last_coord.register_date,
                            creation_user=last_coord.creation_user)