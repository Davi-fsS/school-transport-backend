from business.service.user_phone_service import UserPhoneService
from presentation.dto.CreatePhone import CreatePhone

class UserPhoneController():
    user_phone_service: UserPhoneService

    def __init__(self):
        self.user_phone_service = UserPhoneService()
    
    def get_phone_by_user_id(self, user_id: int):
        return self.user_phone_service.get_user_phone_list(user_id)

    def create_phone(self, user_phone: CreatePhone):
        return self.user_phone_service.create_phone(user_phone)