from business.service.user_point_service import UserPointService
from presentation.dto import SaveCoordinate

class UserPointController():
    user_point_service : UserPointService

    def __init__(self):
        self.user_point_service = UserPointService()
    
    def get_driver_school_by_code(self, code: str):
        return self.user_point_service.get_driver_school_by_code(code)