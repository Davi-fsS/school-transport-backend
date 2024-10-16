from sqlalchemy.orm import Session
from data.model.device_model import DeviceModel
from data.infrastructure.database import get_db

class DeviceRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def create_device(self, device_model: DeviceModel):
        try:
            self.db.add(device_model)
            self.db.commit()
            return device_model.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        
    def get_all_devices(self):
        return self.db.query(DeviceModel).filter(DeviceModel.disabled == False).all()