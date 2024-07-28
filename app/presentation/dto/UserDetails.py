from pydantic import BaseModel
from presentation.dto.User import User
from presentation.dto.Phone import Phone
from presentation.dto.Point import Point
from typing import List

class UserDetails(BaseModel):
    user: User
    phone: List[Phone] = []
    points: List[Point] = []