from sqlalchemy.orm import Session
from data.model.user_point_model import UserPointModel
from data.infrastructure.database import get_db

class UserPointRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_user_point_list(self, user_id: int):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.user_id == user_id).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()
        
    def get_user_point(self, user_id: int, point_id: int):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.user_id == user_id, UserPointModel.point_id == point_id).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()
        
    def delete_user_point(self, user_id: int, point_id: int):
        try:
            user_point = self.get_user_point(user_id, point_id)

            self.db.delete(user_point)
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()

    def create_user_point(self, db_user_point: UserPointModel):
        try:
            self.db.add(db_user_point)
            self.db.commit()
            return db_user_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.db.close()

    