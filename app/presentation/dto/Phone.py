from pydantic import BaseModel

class Phone(BaseModel):
    id: int
    user_id: int
    ddi: str
    ddd: str
    phone : str

