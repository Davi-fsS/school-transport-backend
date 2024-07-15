from pydantic import BaseModel

class UserDto(BaseModel):
    name: str
    email: str
    cpf: str
    cnh: str
    rg: str
    user_type_id: int
    phone: str
    address: str