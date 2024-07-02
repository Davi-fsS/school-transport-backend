from data.repository.user_repository import UserRepository
from presentation.dto.UserDto import UserDto

class UserService():
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
    
    def create_user(self, user: UserDto):
        return self.user_repository.create_user(user)
