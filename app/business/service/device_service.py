from typing import List
from presentation.dto.User import User
from presentation.dto.Device import Device
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

    def get_all_device(self) -> List[Device]:
        devices_dto : List[Device] = []

        devices = self.device_repository.get_all_devices()

        if len(devices) == 0:
            return []

        device_ids = []
        for device in devices:
            device_ids.append(device.id)

        user_devices = self.device_user_repository.get_device_user_list_by_device_list(device_ids)

        user_ids = []
        for user_device in user_devices:
            user_ids.append(user_device.user_id)

        users = self.user_repository.get_user_by_list(user_ids)

        for device in devices:
            user_device = list(filter(lambda ud: ud.device_id == device.id, user_devices))[0]
            
            user = list(filter(lambda u: u.id == user_device.user_id, users))[0]

            user_dto = User(id=user.id, uuid=user.uuid, name=user.name, email=user.email, cpf=user.cpf, cnh=user.cnh, rg=user.rg,
                            user_type_id=user.user_type_id, code=user.code, phones=[])

            devices_dto.append(Device(id=device.id, name=device.name, code=device.code, user=user_dto,
                                      creation_date=device.creation_user, creation_user=device.creation_user))

        return devices_dto

    def create_device(self, device: CreateDevice):
        self.validating_admin(device.user_id)

        device_by_code = self.device_repository.get_device_by_code(device.code)

        if device_by_code is not None:
            raise ValueError("Dispositivo já cadastrado")
        
        self.validating_driver(device.device_user_id)

        device_user = self.device_user_repository.get_device_user_by_user(device.device_user_id)

        if device_user is not None:
            raise ValueError("Usuário já possui dispositivo")

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