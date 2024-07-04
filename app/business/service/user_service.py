from data.repository.user_repository import UserRepository
from presentation.dto.UserDto import UserDto
from validate_docbr import CPF
from validate_rg import validate_rg

class UserService():
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
    
    def create_user(self, user: UserDto):
        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(CPF().validate(user.cpf) == False):
            raise ValueError("CPF inválido")
        
        if(validate_rg.is_valid(user.rg) == False):
            raise ValueError("RG inválido")
        
        if(len(user.uuid) != 28):
            raise ValueError("Firebase uid inválido")

        return self.user_repository.create_user(user)
