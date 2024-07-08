from data.repository.user_repository import UserRepository
from business.service.user_phone_service import UserPhoneService
from presentation.dto.UserDto import UserDto
from data.model.user_model import UserModel
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from validate_docbr import CPF
from validate_rg import validate_rg
import re

class UserService():
    user_repository: UserRepository
    user_phone_service: UserPhoneService

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_phone_service = UserPhoneService()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
    
    def create_user(self, user: UserDto):
        if(user.user_type_id == 1):
            self.validate_administrator(self, user)
        elif(user.user_type_id == 2):
            self.validate_driver(self, user)
        else:
            self.validate_responsible(self, user)

        user_body = UserModel(name=user.name, email=user.email, cpf=user.cpf, cnh=user.cnh, user_type_id=user.user_type_id, rg=user.rg)

        user_id = self.user_repository.create_user(user_body)
    
        phone_body = CreatePhone(user_id=user_id, phone=user.phone)

        self.user_phone_service.create_phone(phone_body)

        return user_id

      
    def update_user_uuid(self, user_data: UpdateUserUuid):
        user = self.user_repository.get_user(user_data.user_id)

        if(user == None):
            raise ValueError("Usuário não existe")
        
        return self.user_repository.update_user_uuid(user_data.user_id, user_data.uuid)
    
    @staticmethod
    def validate_responsible(self, user: UserDto):
        self.validate_email(self, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")
        
        if(user.rg != ""):
            if(self.user_repository.get_user_by_rg(user.rg) != None):
                raise ValueError("RG já cadastrado")

            if(not validate_rg.is_valid(user.rg)):
                raise ValueError("RG inválido")

    @staticmethod
    def validate_administrator(self, user: UserDto):
        self.validate_email(self, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")

    @staticmethod 
    def validate_driver(self, user: UserDto):
        self.validate_email(self, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")

        if(self.user_repository.get_user_by_cnh(user.cnh) != None):
            raise ValueError("CNH já cadastrada")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")

        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")
        
        if(user.rg != ""):
            if(self.user_repository.get_user_by_rg(user.rg) != None):
                raise ValueError("RG já cadastrado")

            if(not validate_rg.is_valid(user.rg)):
                raise ValueError("RG inválido")

    @staticmethod
    def validate_email(self, email: str):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if(self.user_repository.get_user_by_email(email) != None):
            raise ValueError("E-mail já cadastrado")
        
        if(not re.match(regex, email)):
            raise ValueError("E-mail inválido")