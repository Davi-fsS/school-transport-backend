from business.service.user_service import UserService

class UserController():
    user_service: UserService

    def __init__(self):
        self.user_service = UserService()

    def read_all(self):
        return self.user_service.read_all()
    
    def read_by_user(self, id: int):
        return self.user_service.read_by_user(id)