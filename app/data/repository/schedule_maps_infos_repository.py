from sqlalchemy.orm import Session
from data.model.schedule_vehicle_model import ScheduleVehicleModel
from data.infrastructure.database import get_db

class ScheduleMapsInfosModel():
    db: Session

    def __init__(self):
        self.db = next(get_db())