from data.repository.user_phone_repository import UserPhoneRepository
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.UpdatePhone import UpdatePhone
from presentation.dto.Phone import Phone
from data.model.user_phone_model import UserPhoneModel

class UserPhoneService():
    user_phone_repository: UserPhoneRepository

    def __init__(self):
        self.user_phone_repository = UserPhoneRepository()

    def get_user_phone_list(self, user_id: int):
        user_phone_list = self.user_phone_repository.get_user_phone_list(user_id)

        user_phone_list_dto = []
        for user_phone in user_phone_list:
            phone_dto = Phone(id=user_phone.id, user_id=user_phone.user_id, ddi=user_phone.ddd, ddd=user_phone.ddd, phone=user_phone.phone)

            user_phone_list_dto.append(phone_dto)

        return user_phone_list_dto

    def create_phone(self, user_phone: CreatePhone):
        user_phone_to_add = UserPhoneModel(user_id=user_phone.user_id, phone=user_phone.phone, creation_user=2)

        return self.user_phone_repository.create_phone(user_phone_to_add)