from sqlalchemy.orm import Session
from data.model.device_user_model import DeviceUserModel
from presentation.dto.CreateDevice import CreateDevice
from data.model.device_model import DeviceModel
from data.infrastructure.database import get_db

class DeviceRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

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
        
    def get_all_devices(self):
        return self.db.query(DeviceModel).filter(DeviceModel.disabled == False).all()
    
    def get_device_by_code(self, code: str):
        return self.db.query(DeviceModel).filter(DeviceModel.code == code).first()