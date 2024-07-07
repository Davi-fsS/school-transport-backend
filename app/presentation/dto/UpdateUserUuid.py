from pydantic import BaseModel

class UpdateUserUuid(BaseModel):
    user_id: int
    uuid: str