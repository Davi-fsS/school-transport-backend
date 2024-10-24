from typing import List
from sqlalchemy.orm import Session
from data.infrastructure.database import SessionManager
from data.model.user_point_model import UserPointModel

class UserPointRepository():
    db: Session

    def __init__(self):
        self.session_manager = SessionManager()
        self.db = next(self.session_manager.get_db())

    def get_user_point_list(self, user_id: int):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.user_id == user_id, UserPointModel.disabled == False).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def get_user_point_list_by_user_list(self, user_list: List[int]):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.user_id.in_(user_list), UserPointModel.disabled == False).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def get_user_point_list_by_point(self, point_id: int):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.point_id == point_id, UserPointModel.disabled == False).all()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
    
    def get_user_point_by_point(self, point_id: int):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.point_id == point_id, UserPointModel.disabled == False).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def get_user_point(self, user_id: int, point_id: int):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.user_id == user_id, UserPointModel.point_id == point_id, UserPointModel.disabled == False).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def get_user_point_by_code(self, code: str):
        try:
            return self.db.query(UserPointModel).filter(UserPointModel.code == code, UserPointModel.disabled == False).first()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def delete_user_point(self, user_id: int, point_id: int):
        try:
            user_point = self.get_user_point(user_id, point_id)
            user_point.disabled = True

            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)
        
    def delete_user_point_list_by_point(self, point_id: int):
        try:
            user_point_list = self.get_user_point_list_by_point(point_id)

            for user_point in user_point_list:
                user_point.disabled = True 
                self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.session_manager.close(self.db)

    def create_user_point(self, db_user_point: UserPointModel):
        try:
            self.db.add(db_user_point)
            self.db.commit()
            return db_user_point.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.session_manager.close(self.db)

    