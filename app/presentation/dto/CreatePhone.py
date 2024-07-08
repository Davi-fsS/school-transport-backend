from pydantic import BaseModel

class CreatePhone(BaseModel):
    user_id: int
    phone: str