from data.repository.user_phone_repository import UserPhoneRepository
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.UpdatePhone import UpdatePhone
from data.model.user_phone_model import UserPhoneModel

class UserPhoneService():
    user_phone_repository: UserPhoneRepository

    def __init__(self):
        self.user_phone_repository = UserPhoneRepository()

    def create_phone(self, user_phone: CreatePhone):
        user_phone_to_add = UserPhoneModel(user_id=user_phone.user_id, phone=user_phone.phone, creation_user=2)

        return self.user_phone_repository.create_phone(user_phone_to_add)