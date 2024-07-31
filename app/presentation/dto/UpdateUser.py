from pydantic import BaseModel
from presentation.dto.UpdatePoint import UpdatePoint

class UpdateUser(BaseModel):
    id: int
    name: str
    email: str
    cpf: str
    cnh: str | None
    rg: str | None
    user_type_id: int
