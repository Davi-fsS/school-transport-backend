from fastapi import FastAPI, status, HTTPException
from presentation.controller.user_controller import UserController
from presentation.controller.user_type_controller import UserTypeController
from presentation.dto.UserDto import UserDto

app = FastAPI()

user_controller = UserController()
user_type_controller = UserTypeController()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/user",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDto):
    return user_controller.create_user(user)

@app.get("/user-by-id/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int):
    user = user_controller.read_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@app.get("/user-type-by-id/{type_id}", status_code=status.HTTP_200_OK)
async def read_user_type_by_id(type_id: int):
    user_type = user_type_controller.read_type(type_id)
    if user_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    return user_type