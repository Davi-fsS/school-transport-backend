from pydantic import BaseModel
from presentation.dto.User import User
from presentation.dto.Phone import Phone
from presentation.dto.Point import Point
from typing import List

class DriverDetails(BaseModel):
    user: User
    phone: List[Phone] | None
    school: Point