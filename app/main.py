from fastapi import FastAPI, status, HTTPException, Header
from presentation.controller.user_controller import UserController
from presentation.controller.user_type_controller import UserTypeController
from presentation.controller.user_phone_controller import UserPhoneController
from presentation.controller.student_controller import StudentController
from presentation.dto.UserDto import UserDto
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://192.168.0.149",
    "http://192.168.0.150"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_controller = UserController()
user_type_controller = UserTypeController()
user_phone_controller = UserPhoneController()
student_controller = StudentController()

# USER ENDPOINTS
@app.post("/user/create",status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDto):
    try:
        return user_controller.create_user(user)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/user/update-uuid",status_code=status.HTTP_200_OK)
async def update_user_uuid(user_data: UpdateUserUuid):
    try:
        return user_controller.update_user_uuid(user_data)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/user/by-id/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int):
    user = user_controller.read_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

# USER_TYPE ENDPOINTS
@app.get("/user-type/by-id/{type_id}", status_code=status.HTTP_200_OK)
async def read_user_type_by_id(type_id: int):
    user_type = user_type_controller.read_type(type_id)
    if user_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo não encontrado")
    return user_type

# USER_PHONE ENDPOINTS
@app.post("/user-phone/create", status_code=status.HTTP_201_CREATED)
async def create_user_phone(user_phone: CreatePhone):
    try:
        return user_phone_controller.create_phone(user_phone)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
# STUDENT ENDPOINTS
@app.post("/student/create",status_code=status.HTTP_201_CREATED)
async def create_user(student: CreateStudent):
    try:
        return student_controller.create_student(student=student)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="192.168.15.5", port=8000)