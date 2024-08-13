from pydantic import BaseModel

class DriverAssociation(BaseModel):
    user_id: int
    point_id: int