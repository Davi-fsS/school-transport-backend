from pydantic import BaseModel

class GetHistoricByDate(BaseModel):
    date: str
    user_id: int