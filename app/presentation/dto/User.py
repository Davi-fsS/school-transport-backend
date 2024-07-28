from pydantic import BaseModel
from presentation.dto.CreatePoint import CreatePoint

class User(BaseModel):
    id: int
    uuid: str = ""
    name: str = ""
    email: str = ""
    cpf: str = ""
    cnh: str = ""
    rg: str = ""
    user_type_id: int