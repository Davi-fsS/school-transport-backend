from typing import List
from business.service.point_service import PointService
from presentation.dto.CreateSchool import CreateSchool

class PointController():
    point_service: PointService

    def __init__(self):
        self.point_service = PointService()

    def create_school(self, school: CreateSchool):
        return self.point_service.create_school(school)