from presentation.dto.User import User
from business.service.user_service import UserService
from data.repository.schedule_user_repository import ScheduleUserRepository

class ScheduleUserService():
    schedule_user_repository: ScheduleUserRepository
    user_service: UserService

    def __init__(self):
        self.schedule_user_repository = ScheduleUserRepository()
        self.user_service = UserService()

    def get_schedule_user_by_schedule_id(self, schedule_id: int):
        return self.schedule_user_repository.get_schedule_user_by_schedule_id(schedule_id)
    
    def get_user_by_schedule_id(self, schedule_id: int):
        schedule_user = self.schedule_user_repository.get_schedule_user_by_schedule_id(schedule_id)

        if(schedule_user is None):
            raise ValueError("Não existe usuário associado a esta viagem")
        
        user = self.user_service.get_user(schedule_user.user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário não permitido")

        user_dto = User(id=user.id, uuid=user.uuid, name=user.name,
                        email=user.email, cpf=user.cpf, cnh=user.cnh,
                        rg=user.rg, user_type_id=user.user_type_id, code= user.code)
        
        return user_dto