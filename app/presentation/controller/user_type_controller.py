from business.service.user_type_service import UserTypeService

class UserTypeController():
    user_type_service: UserTypeService

    def __init__(self):
        self.user_type_service = UserTypeService()
    
    def read_type(self, type_id: int):
        return self.user_type_service.get_type(type_id)