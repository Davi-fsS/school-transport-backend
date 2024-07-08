from business.service.user_phone_service import UserPhoneService
from presentation.dto.CreatePhone import CreatePhone

class UserPhoneController():
    user_phone_service: UserPhoneService

    def __init__(self):
        self.user_phone_service = UserPhoneService()
    
    def create_phone(self, user_phone: CreatePhone):
        return self.user_phone_service.create_phone(user_phone)