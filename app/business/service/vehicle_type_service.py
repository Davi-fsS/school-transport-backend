from data.repository.vehicle_type_repository import VehicleTypeRepository

class VehicleTypeService():
    vehice_type_repository: VehicleTypeRepository

    def __init__(self):
        self.vehice_type_repository = VehicleTypeRepository()

    def get_type(self, type_id: int):
        return self.vehice_type_repository.get_type(type_id)
