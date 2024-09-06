from pydantic import BaseModel
from presentation.dto.Point import Point

class SchoolAssociation(BaseModel):
    point: Point
    code: str = ""