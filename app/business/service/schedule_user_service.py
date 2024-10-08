from data.repository.schedule_repository import ScheduleRepository
from business.service.user_phone_service import UserPhoneService
from presentation.dto.User import User
from business.service.user_service import UserService
from data.repository.schedule_user_repository import ScheduleUserRepository

class ScheduleUserService():
    schedule_user_repository: ScheduleUserRepository
    schedule_repository: ScheduleRepository
    user_phone_service: UserPhoneService
    user_service: UserService

    def __init__(self):
        self.schedule_user_repository = ScheduleUserRepository()
        self.user_service = UserService()
        self.user_phone_service = UserPhoneService()
        self.schedule_repository = ScheduleRepository()

    def get_schedule_user_by_schedule_id(self, schedule_id: int):
        return self.schedule_user_repository.get_schedule_user_by_schedule_id(schedule_id)
    
    def get_schedule_user_list_by_user_id(self, user_id: int):
        return self.schedule_user_repository.get_schedule_user_list_by_user_id(user_id)

    def get_current_schedule_by_user(self, user_id: int):
        schedule_users_list = self.schedule_user_repository.get_schedule_user_list_by_user_id(user_id)

        schedule_ids = []
        for schedule_user in schedule_users_list:
            schedule_ids.append(schedule_user.schedule_id)

        current_schedule_by_list = self.schedule_repository.get_schedule_list_in_progress_by_list(schedule_ids)

        return current_schedule_by_list[0]
    
    def get_user_by_schedule_id(self, schedule_id: int):
        schedule_user = self.schedule_user_repository.get_schedule_user_by_schedule_id(schedule_id)

        if(schedule_user is None):
            raise ValueError("Não existe usuário associado a esta viagem")
        
        user = self.user_service.get_user(schedule_user.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")
        
        user_phone_list = self.user_phone_service.get_user_phone_list(user.id)

        user_dto = User(id=user.id, uuid=user.uuid, name=user.name,
                        email=user.email, cpf=user.cpf, cnh=user.cnh,
                        rg=user.rg, user_type_id=user.user_type_id, 
                        code= user.code, phones=user_phone_list)
        
        return user_dto