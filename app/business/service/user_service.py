from data.repository.user_repository import UserRepository
from business.service.user_phone_service import UserPhoneService
from business.service.point_service import PointService
from business.service.user_point_service import UserPointService
from presentation.dto.UserDto import UserDto
from data.model.user_model import UserModel
from data.model.point_model import PointModel
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from validate_docbr import CPF
from validate_rg import validate_rg
import re

class UserService():
    user_repository: UserRepository
    user_phone_service: UserPhoneService
    point_service: PointService
    user_point_service: UserPointService

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_phone_service = UserPhoneService()
        self.point_service = PointService()
        self.user_point_service = UserPointService()

    def get_user(self, user_id: int):
        return self.user_repository.get_user(user_id)
    
    def create_user(self, user: UserDto):
        if(user.user_type_id == 1):
            self.validate_administrator(self, user)
        elif(user.user_type_id == 2):
            self.validate_driver(self, user)
        else:
            self.validate_responsible(self, user)

        user_id = self.creating_user(self, user=user)
    
        self.creating_user_phone(self, user_id=user_id, phone=user.phone)

        self.creating_user_point(user_id=user_id, name=user.name, address=user.address)

        return user_id
      
    def update_user_uuid(self, user_data: UpdateUserUuid):
        user = self.user_repository.get_user(user_data.user_id)

        if(user == None):
            raise ValueError("Usuário não existe")
        
        return self.user_repository.update_user_uuid(user_data.user_id, user_data.uuid)
    
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

    def validate_administrator(self, user: UserDto):
        self.validate_email(self, user.email)

        if(user.user_type_id == 0):
            raise ValueError("Tipo de Usuário não encontrado")
        
        if(self.user_repository.get_user_by_cpf(user.cpf) != None):
            raise ValueError("CPF já cadastrado")
        
        if(not CPF().validate(user.cpf)):
            raise ValueError("CPF inválido")

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

    def validate_email(self, email: str):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if(self.user_repository.get_user_by_email(email) != None):
            raise ValueError("E-mail já cadastrado")
        
        if(not re.match(regex, email)):
            raise ValueError("E-mail inválido")
        
    def creating_user(self, user: UserDto):
        user_body = UserModel(name=user.name, email=user.email, cpf=user.cpf, cnh=user.cnh, user_type_id=user.user_type_id, rg=user.rg)

        user_id = self.user_repository.create_user(user_body)

        return user_id

    def creating_user_phone(self, user_id: int, phone: str):
        phone_body = CreatePhone(user_id=user_id, phone=phone)

        self.user_phone_service.create_phone(phone_body)

    def creating_user_point(self, user_id: int, name: str, address: str):
        point_body = PointModel(name=f"Casa {name}", address=address, point_type_id=1, description=f"Endereço principal de {name}")

        point_id = self.point_service.create_point(point_body)

        self.user_point_service.create_user_point(user_id=user_id, point_id=point_id, is_favorite=True)