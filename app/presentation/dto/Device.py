from datetime import datetime
from pydantic import BaseModel

from presentation.dto.User import User

class Device(BaseModel):
    id: int
    name: str
    code: str
    user: User
    creation_date: datetime
    creation_user: int