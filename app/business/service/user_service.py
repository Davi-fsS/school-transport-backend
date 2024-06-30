from data.repository.user_repository import UserRepository

class UserService():
    user_repository : UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def read_all(self):
        return self.user_repository.read_all()
    
    def read_by_user(self, id: int):
        return self.user_repository.read_by_id(id)