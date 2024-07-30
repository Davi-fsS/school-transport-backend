from typing import List
from business.service.point_service import PointService
from presentation.dto.CreatePoint import CreatePoint
from presentation.dto.UpdatePoint import UpdatePoint

class PointController():
    point_service: PointService

    def __init__(self):
        self.point_service = PointService()

    def get_all_school_list(self):
        return self.point_service.get_all_school_list()

    def create_point(self, point: CreatePoint):
        return self.point_service.create_point(point)
    
    def update_point(self, point: UpdatePoint):
        return self.point_service.update_point(point)
    
    def delete_point(self, point_id: int):
        return self.point_service.delete_point(point_id)
