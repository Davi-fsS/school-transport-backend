from sqlalchemy.orm import Session
from data.model.point_model import PointModel
from presentation.dto.UpdateSchool import UpdateSchool
from presentation.dto.UpdatePoint import UpdatePoint
from data.infrastructure.database import get_db
from datetime import datetime
from typing import List

class PointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_points_by_point_list(self, point_id_list: List[int]):
        try:
            points = self.db.query(PointModel).filter(PointModel.id.in_(point_id_list)).all()
            return points
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def get_point(self, point_id: int):
        try:
            return self.db.query(PointModel).filter(PointModel.id == point_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
    
    def get_school(self, school_id: int):
        try:
            return self.db.query(PointModel).filter(PointModel.id == school_id and PointModel.point_type_id == 2).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def get_all_school_list(self):
        try:
            return self.db.query(PointModel).filter(PointModel.point_type_id == 2).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")

    def create_point(self, db_point: PointModel):
        try:
            self.db.add(db_point)
            self.db.commit()
            return db_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def update_point(self, lat: float, lng: float, point_update: UpdatePoint):
        try:
            point = self.get_school(point_update.id)

            point.name = point_update.name
            point.address = point_update.address
            point.city = point_update.city
            point.neighborhood = point_update.neighborhood
            point.state = point_update.state
            point.description = point_update.description
            point.lat = lat
            point.lng = lng
            point.change_date = datetime.now()

            self.db.commit()
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

    def delete_point(self, point_id: int):
        try:
            point = self.get_point(point_id)
            self.db.delete(point)
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    