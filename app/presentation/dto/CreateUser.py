from pydantic import BaseModel
from presentation.dto.CreatePoint import CreatePoint

class CreateUser(BaseModel):
    name: str
    email: str
    cpf: str
    cnh: str
    rg: str
    user_type_id: int
    phone: str
    address: CreatePoint