from data.repository.user_point_repository import UserPointRepository
from presentation.dto.CreatePhone import CreatePhone
from data.model.user_point_model import UserPointModel

class UserPointService():
    user_point_repository: UserPointRepository

    def __init__(self):
        self.user_point_repository = UserPointRepository()

    def create_user_point(self, user_id: int, point_id: int, is_favorite: bool):
        user_point = UserPointModel(user_id=user_id, point_id=point_id, favorite=is_favorite, creation_user=2)

        return self.user_point_repository.create_user_point(user_point)
    
    def get_user_point_list(self, user_id: int):
        return self.user_point_repository.get_user_point_list(user_id)