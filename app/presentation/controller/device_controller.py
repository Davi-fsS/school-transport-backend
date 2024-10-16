from presentation.dto.UpdateDevice import UpdateDevice
from presentation.dto.CreateDevice import CreateDevice
from business.service.device_service import DeviceService
from presentation.dto import SaveCoordinate
from business.service.coordinate_service import CoordinateService

class DeviceController():
    device_service : DeviceService

    def __init__(self):
        self.device_service = DeviceService()

    def create_device(self, device: CreateDevice):
        return self.device_service.create_device(device)
    
    def update_device(self, device: UpdateDevice):
        return self.device_service.update_device(device)