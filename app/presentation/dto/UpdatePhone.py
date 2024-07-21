from pydantic import BaseModel

class UpdatePhone(BaseModel):
    id: int
    user_id: int
    phone: str