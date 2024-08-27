from pydantic import BaseModel
from presentation.dto.Vehicle import Vehicle
from presentation.dto.Point import Point

class PointVehicle(BaseModel):
    id: int
    code: str
    vehicle: Vehicle = []
    point: Point = []