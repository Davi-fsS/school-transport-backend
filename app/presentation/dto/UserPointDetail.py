from pydantic import BaseModel

from presentation.dto.Point import Point
from presentation.dto.User import User

class UserPointDetail(BaseModel):
    user: User
    point: Point
    code: str