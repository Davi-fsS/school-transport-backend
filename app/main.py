from fastapi import FastAPI, HTTPException, Depends, status
from presentation.controller.user_controller import UserController
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime

from data.infrastructure.database import engine, SessionLocal, Base

from data.model.user_model import UserModel

app = FastAPI()
Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    uuid: str
    name: str
    email: str
    cpf: str
    cnh: str
    rg: str
    user_type_id: int
    creation_user: int
    change_date: datetime
    change_user: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependecy):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()