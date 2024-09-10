from typing import List
from presentation.dto.UserPointDetail import UserPointDetail
from data.repository.point_repository import PointRepository
from presentation.dto.Point import Point
from presentation.dto.Phone import Phone
from data.repository.user_phone_repository import UserPhoneRepository
from presentation.dto.User import User
from data.repository.user_repository import UserRepository
from data.repository.user_point_repository import UserPointRepository
from data.model.user_point_model import UserPointModel

class UserPointService():
    user_point_repository: UserPointRepository
    user_repository: UserRepository
    user_phone_repository: UserPhoneRepository
    point_repository: PointRepository

    def __init__(self):
        self.user_point_repository = UserPointRepository()
        self.user_repository = UserRepository()
        self.user_phone_repository = UserPhoneRepository()
        self.point_repository = PointRepository()

    def create_user_point(self, user_id: int, point_id: int, is_favorite: bool, code: str = ""):
        user_point = UserPointModel(user_id=user_id, point_id=point_id, favorite=is_favorite, creation_user=2, code=code)

        return self.user_point_repository.create_user_point(user_point)
    
    def get_user_point_list(self, user_id: int):
        return self.user_point_repository.get_user_point_list(user_id)
    
    def get_user_point_list_by_user_list(self, user_list: List[int]):
        return self.user_point_repository.get_user_point_list_by_user_list(user_list)
    
    def delete_user_point(self, user_id: int, point_id: int):
        return self.user_point_repository.delete_user_point(user_id, point_id)
    
    def delete_user_point_list_by_point(self, point_id: int):
        return self.user_point_repository.delete_user_point_list_by_point(point_id)
    
    def get_driver_school_by_code(self, code: str):
        user_phones_dto : List[Phone] = []

        user_point = self.user_point_repository.get_user_point_by_code(code)

        if(user_point is None):
            raise ValueError("Código inválido")
        
        user = self.user_repository.get_user(user_point.user_id)

        if(user is None):
            raise ValueError("Usuário não encontrado")

        if(user.user_type_id == 3):
            raise ValueError("Usuário não é um motorista")
        
        user_phones = self.user_phone_repository.get_user_phone_list(user.id)

        if(len(user_phones_dto) > 0):
            for user_phone in user_phones:
                phone_dto = Phone(id=user_phone.id, user_id=user_phone.user_id, ddi=user_phone.ddi, ddd=user_phone.ddd, phone=user_phone.phone)
                user_phones_dto.append(phone_dto)
        
        user_dto = User(id=user.id, uuid=user.uuid, name=user.name, email=user.email, cpf=user.cpf, cnh=user.cnh, rg=user.rg,
                        user_type_id=user.user_type_id, code=user.code, phones=user_phones_dto)
        
        point = self.point_repository.get_point(user_point.point_id)

        if(point is None):
            raise ValueError("Não foi identificado um endereço a este código")
        
        if(point.point_type_id != 2):
            raise ValueError("Não foi identificado uma escola a este código")

        point_dto = Point(id=point.id, name=point.name, address=point.address, lat=point.lat, lng=point.lng, alt=point.alt,
                          city=point.city, neighborhood=point.neighborhood, state=point.state, description=point.description,
                          point_type_id=point.point_type_id)
        
        user_point_detail_dto = UserPointDetail(point=point_dto, user=user_dto, code=code)

        return user_point_detail_dto