from typing import List
from sqlalchemy.orm import Session
from data.model.device_user_model import DeviceUserModel
from data.model.device_model import DeviceModel
from data.infrastructure.database import get_db

class DeviceUserRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_device_user(self, device_user_model: DeviceUserModel):
        try:
            self.db.add(device_user_model)
            self.db.commit()
            return device_user_model.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def get_device_user_by_device(self, device_id: int):
        return self.db.query(DeviceUserModel).filter(DeviceUserModel.device_id == device_id, DeviceUserModel.disabled == False).first()

    def get_device_user_by_user(self, user_id: int):
        return self.db.query(DeviceUserModel).filter(DeviceUserModel.user_id == user_id, DeviceUserModel.disabled == False).first()

    def get_device_user_list_by_device_list(self, device_list: List[int]):
        return self.db.query(DeviceUserModel).filter(DeviceUserModel.device_id.in_(device_list), DeviceUserModel.disabled == False).all()