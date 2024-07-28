from pydantic import BaseModel

class Phone(BaseModel):
    id: int
    user_id: int
    ddi: str | None
    ddd: str | None
    phone : str | None

