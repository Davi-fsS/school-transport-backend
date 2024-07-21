from sqlalchemy.orm import Session
from data.model.point_model import PointModel
from presentation.dto.UpdateSchool import UpdateSchool
from data.infrastructure.database import get_db
from datetime import datetime

class PointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_point(self, point_id: int):
        return self.db.query(PointModel).filter(PointModel.id == point_id).first()

    def create_point(self, db_point: PointModel):
        try:
            self.db.add(db_point)
            self.db.commit()
            return db_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def update_school(self, lat: float, lng: float, school_update: UpdateSchool):
        try:
            school = self.get_school(school_update.id)

            school.name = school_update.name
            school.address = school_update.address
            school.city = school_update.city
            school.neighborhood = school_update.neighborhood
            school.state = school_update.state
            school.description = school_update.description
            school.lat = lat
            school.lng = lng
            school.change_date = datetime.now()

            self.db.commit()
            return school.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")

    def delete_school(self, school_id: int):
        try:
            student = self.get_school(school_id)
            self.db.delete(student)
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    