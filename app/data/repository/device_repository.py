from datetime import datetime
from sqlalchemy.orm import Session
from data.repository.device_user_repository import DeviceUserRepository
from presentation.dto.UpdateDevice import UpdateDevice
from data.model.device_user_model import DeviceUserModel
from presentation.dto.CreateDevice import CreateDevice
from data.model.device_model import DeviceModel
from data.infrastructure.database import get_db

class DeviceRepository():
    db: Session
    device_user_repository: DeviceUserRepository

    def __init__(self):
        self.db = next(get_db())
        self.device_user_repository = DeviceUserRepository()

    def create_device(self, body: CreateDevice):
        try:
            device_model = DeviceModel(code=body.code, name=body.name, creation_user=body.user_id)

            self.db.add(device_model)
            self.db.flush()

            device_user_model = DeviceUserModel(device_id=device_model.id, user_id=body.device_user_id, creation_user=body.user_id)

            self.db.add(device_user_model)

            self.db.commit()
            return device_model.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
    
    def update_device(self, body: UpdateDevice):
        try:
            device_model = self.get_device_by_id(body.id)

            device_model.code = body.code
            device_model.name = body.name
            device_model.change_date = datetime.now()
            device_model.change_user = body.user_id

            self.db.flush()

            device_user_model = self.device_user_repository.get_device_user_by_device(device_model.id)

            device_user_model.user_id = body.device_user_id

            self.db.commit()
            return device_model.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def get_all_devices(self):
        return self.db.query(DeviceModel).filter(DeviceModel.disabled == False).all()
    
    def get_device_by_code(self, code: str) -> DeviceModel:
        return self.db.query(DeviceModel).filter(DeviceModel.code == code, DeviceModel.disabled == False).first()
    
    def get_device_by_id(self, id: int) -> DeviceModel:
        return self.db.query(DeviceModel).filter(DeviceModel.id == id, DeviceModel.disabled == False).first()