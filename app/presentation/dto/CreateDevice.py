from pydantic import BaseModel

class CreateDevice(BaseModel):
    code: str
    name: str
    device_user_id: int
    user_id: int
