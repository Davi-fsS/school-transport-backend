from data.repository.user_repository import UserRepository
from presentation.dto.UserDto import UserDto
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from validate_docbr import CPF
from validate_rg import validate_rg

class UserService():
    user_repository: UserRepository

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
    
    def create_user(self, user: UserDto):
        if(user.user_type_id == 1):
            self.validate_administrator(self, user)
        elif(user.user_type_id == 2):
            self.validate_driver(self, user)
        else:
            self.validate_responsible(self, user)

        return self.user_repository.create_user(user)
    
    @staticmethod
    def validate_responsible(self, user: UserDto):
        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_email(user.email) != None):
            raise ValueError("E-mail já cadastrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(CPF().validate(user.cpf) == False):
            raise ValueError("CPF inválido")
        
        if(user.rg != ""):
            if(self.user_repository.get_user_by_rg(user.rg) != None):
                raise ValueError("RG já cadastrado")

            if(validate_rg.is_valid(user.rg) == False):
                raise ValueError("RG inválido")

    @staticmethod
    def validate_administrator(self, user: UserDto):
        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_email(user.email) != None):
            raise ValueError("E-mail já cadastrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(CPF().validate(user.cpf) == False):
            raise ValueError("CPF inválido")

    @staticmethod 
    def validate_driver(self, user: UserDto):
        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_email(user.email) != None):
            raise ValueError("E-mail já cadastrado")

        if(self.user_repository.get_user_by_cnh(user.cnh) != None):
            raise ValueError("CNH já cadastrada")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")

        if(CPF().validate(user.cpf) == False):
            raise ValueError("CPF inválido")
        
        if(user.rg != ""):
            if(self.user_repository.get_user_by_rg(user.rg) != None):
                raise ValueError("RG já cadastrado")

            if(validate_rg.is_valid(user.rg) == False):
                raise ValueError("RG inválido")

    def update_user_uuid(self, user_data: UpdateUserUuid):
        user = self.user_repository.get_user(user_data.user_id)

        if(user == None):
            raise ValueError("Usuário não existe")
        
        return self.user_repository.update_user_uuid(user_data.user_id, user_data.uuid)