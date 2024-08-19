from sqlalchemy.orm import Session
from data.model.vehicle_model import VehicleModel
from presentation.dto.UpdateVehicle import UpdateVehicle
from data.infrastructure.database import get_db

class VehicleRepository():
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_vehicle(self, id: int):
        try:
            vehicle = self.db.query(VehicleModel).filter(VehicleModel.id == id).first()
            
            if vehicle is None:
                raise ValueError("Veículo não encontrado")

            return vehicle
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()

    def get_all_vehicle(self):
        try:
            all_vehicle = self.db.query(VehicleModel).all()

            return all_vehicle
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()

    def get_vehicle_by_plate(self, plate: str):
        try:
            vehicle = self.db.query(VehicleModel).filter(VehicleModel.plate == plate).first()
            
            return vehicle
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")    
        finally:
            self.db.close()

    def get_vehicle_by_driver(self, user_id: int):
        try:
            vehicle = self.db.query(VehicleModel).filter(VehicleModel.user_id == user_id).first()
            
            return vehicle
        except:
            self.db.rollback()
            raise ValueError("Erro ao fazer a leitura no sistema")
        finally:
            self.db.close()

    def create_vehicle(self, db_vehicle: VehicleModel):
        try:
            self.db.add(db_vehicle)
            self.db.commit()
            return db_vehicle.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.db.close()
        
    def update_vehicle(self, vehicle_update: UpdateVehicle):
        try:
            vehicle = self.get_vehicle(vehicle_update.id)
            vehicle.plate = vehicle_update.plate
            vehicle.user_id = vehicle_update.user_id
            vehicle.model = vehicle_update.model
            vehicle.color = vehicle_update.color
            vehicle.year = vehicle_update.year
            self.db.commit()
            return vehicle.id
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.db.close()

    def delete_vehicle(self, vehicle_id: int):
        try:
            vehicle = self.get_vehicle(vehicle_id)
            self.db.delete(vehicle)
            self.db.commit()
        except:
            self.db.rollback()
            raise ValueError("Erro ao salvar no sistema")
        finally:
            self.db.close()
    