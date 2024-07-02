from pydantic import BaseModel

class UserDto(BaseModel):
    uuid: str
    name: str
    email: str
    cpf: str
    cnh: str
    rg: str
    user_type_id: int
    # creation_date: Datetime
    creation_user: int
    # change_date: Datetime
    change_user: int