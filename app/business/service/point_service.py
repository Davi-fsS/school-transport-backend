from data.repository.point_repository import PointRepository
from presentation.dto.CreatePhone import CreatePhone
from data.model.point_model import PointModel

class PointService():
    point_repository: PointRepository

    def __init__(self):
        self.point_repository = PointRepository()

    def create_point(self, point: PointModel):
        return self.point_repository.create_point(point)
