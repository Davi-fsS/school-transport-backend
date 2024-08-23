from pydantic import BaseModel
from presentation.dto.Vehicle import Vehicle
from presentation.dto.Point import Point
from typing import List

class VehiclePoint(BaseModel):
    vehicle: Vehicle
    school: Point