from data.repository.user_repository import UserRepository
from presentation.dto.UpdateDevice import UpdateDevice
from data.model.device_model import DeviceModel
from presentation.dto.CreateDevice import CreateDevice
from data.repository.device_user_repository import DeviceUserRepository
from data.repository.device_repository import DeviceRepository

class DeviceService():
    device_repository: DeviceRepository
    device_user_repository: DeviceUserRepository
    user_repository: UserRepository

    def __init__(self):
        self.device_repository = DeviceRepository()
        self.device_user_repository = DeviceUserRepository()
        self.user_repository = UserRepository()

    def get_all_device(self):
        return self.device_repository.get_all_devices()

    def create_device(self, device: CreateDevice):
        self.validating_admin(device.user_id)

        device_by_code = self.device_repository.get_device_by_code(device.code)

        if device_by_code is not None:
            raise ValueError("Dispositivo já cadastrado")
        
        self.validating_driver(device.device_user_id) 

        return self.device_repository.create_device(device)
    
    def delete_device(self, id: int):
        device = self.device_repository.get_device_by_id(id)

        if device is None:
            raise ValueError("Dispositivo inválido")
        
        return self.device_repository.delete_device(device.id)

    def update_device(self, device: UpdateDevice):
        self.validating_admin(device.user_id)

        device_by_id = self.device_repository.get_device_by_id(device.id)
        
        device_by_code = self.device_repository.get_device_by_code(device.code)

        if device_by_code is not None and device_by_code.id != device_by_id.id :
            raise ValueError("Código já cadastrado em outro dispositivo")
        
        self.validating_driver(device.device_user_id) 

        return self.device_repository.update_device(device)

    def validating_admin(self, user_id: int):
        user = self.user_repository.get_user(user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id != 1):
            raise ValueError("Usuário não é um administrador")
        
        return user
    
    def validating_driver(self, user_id: int):
        user = self.user_repository.get_user(user_id)

        if(user is None):
            raise ValueError("Usuário inválido")

        if(user.user_type_id == 3):
            raise ValueError("Usuário não é um motorista")
        
        return user