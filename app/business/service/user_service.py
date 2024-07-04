from data.repository.user_repository import UserRepository
from presentation.dto.UserDto import UserDto
from validate_docbr import CPF

class UserService():
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
    
    def create_user(self, user: UserDto):
        if(user.user_type_id == 0):
            raise ValueError

        if(len(user.cpf) != 11 or len(user.cpf) != 11): 
            raise ValueError
        
        if(CPF().validate(user.cpf) == False):
            raise ValueError

        return self.user_repository.create_user(user)
