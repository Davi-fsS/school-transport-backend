from fastapi import FastAPI
from presentation.controller.user_controller import UserController

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/real-all")
def real_all_user():
    user_controller = UserController()
    return user_controller.read_all()

@app.get("/user/real-by-id")
def real_all_user():
    user_controller = UserController()
    return {user_controller.read_by_user(2)}