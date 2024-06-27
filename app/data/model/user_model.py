from abc import ABC
from app.data.model.user_type_model import UserType
from data.helpers.errors.model_errors import EntityError

class User(ABC):
    id: int
    uuid: str
    name: str
    email: str
    cpf: str
    cnh: str
    rg: str
    user_type: UserType

    def __init__(self, id: int, uuid: str, name: str, email: str, cpf: str, cnh: str, rg: str, user_type: UserType):
        EntityError.validate_field(id, int)
        self.id = id

        EntityError.validate_field(uuid, str)
        self.uuid = uuid

        EntityError.validate_field(name, str)
        self.name = name

        EntityError.validate_field(email, str)
        self.email = email

        EntityError.validate_field(cpf, str)
        self.cpf = cpf

        EntityError.validate_field(cnh, str)
        self.cnh = cnh

        EntityError.validate_field(rg, str)
        self.rg = rg

        EntityError.validate_field(user_type, UserType)
        self.user_type = user_type

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email,
            "cpf": self.cpf,
            "cnh": self.cnh,
            "rg": self.rg,
            "user_type": self.user_type.to_dict()
        }