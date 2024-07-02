from pydantic import BaseModel
from datetime import datetime

class UserDto(BaseModel):
    uuid: str
    name: str
    email: str
    cpf: str
    cnh: str
    rg: str
    user_type_id: int
    creation_user: int
    change_date: datetime
    change_user: int