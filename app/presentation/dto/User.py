from pydantic import BaseModel
from presentation.dto.Phone import Phone
from typing import List

class User(BaseModel):
    id: int
    uuid: str | None
    name: str = ""
    email: str = ""
    cpf: str = ""
    cnh: str | None
    rg: str = ""
    user_type_id: int
    code: str | None
    phones: List[Phone] | None