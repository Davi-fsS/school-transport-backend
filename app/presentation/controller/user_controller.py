from business.service.user_service import UserService
from presentation.dto.UserDto import UserDto
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from presentation.dto.UpdateUser import UpdateUser

class UserController():
    user_service: UserService

    def __init__(self):
        self.user_service = UserService()
    
    def read_user(self, user_id: int):
        return self.user_service.get_user(user_id)
    
    def read_all_drivers(self):
        return self.user_service.get_all_drivers()
    
    def read_user_by_email(self, email: str):
        return self.user_service.get_user_by_email(email)

    def create_user(self, user: UserDto):
        return self.user_service.create_user(user)
    
    def update_user_uuid(self, user_data: UpdateUserUuid):
        return self.user_service.update_user_uuid(user_data)
    
    def update_user(self, user: UpdateUser):
        return self.user_service.update_user(user)