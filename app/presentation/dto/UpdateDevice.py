from pydantic import BaseModel

class UpdateDevice(BaseModel):
    id: int
    code: str
    name: str
    device_user_id: int
    user_id: int
