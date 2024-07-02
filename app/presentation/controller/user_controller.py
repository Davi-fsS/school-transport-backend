from business.service.user_service import UserService

class UserController():
    user_service: UserService

    def __init__(self):
        self.user_service = UserService()
    
    def read_user(self, user_id: int):
        return self.user_service.get_user(user_id)
