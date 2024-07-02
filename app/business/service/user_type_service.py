from data.repository.user_type_repository import UserTypeRepository

class UserTypeService():
    user_type_repository: UserTypeRepository

    def __init__(self):
        self.user_type_repository = UserTypeRepository()

    def get_type(self, type_id: int):
        return self.user_type_repository.get_type(type_id)
