from fastapi import FastAPI, status, HTTPException, Header
from presentation.controller.user_controller import UserController
from presentation.controller.user_type_controller import UserTypeController
from presentation.controller.user_phone_controller import UserPhoneController
from presentation.controller.student_controller import StudentController
from presentation.controller.vehicle_controller import VehicleController
from presentation.controller.point_controller import PointController
from presentation.dto.CreateUser import CreateUser
from presentation.dto.CreateStudent import CreateStudent
from presentation.dto.CreatePhone import CreatePhone
from presentation.dto.CreatePoint import CreatePoint
from presentation.dto.DriverAssociation import DriverAssociation
from presentation.dto.UpdateUser import UpdateUser
from presentation.dto.UpdateStudent import UpdateStudent
from presentation.dto.UpdateUserUuid import UpdateUserUuid
from presentation.dto.CreateVehicle import CreateVehicle
from presentation.dto.UpdateVehicle import UpdateVehicle
from presentation.dto.StudentAssociation import StudentAssociation
from presentation.dto.UpdatePoint import UpdatePoint
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://192.168.0.149",
    "http://192.168.0.150",
    "https://school-transport-backend-3fec5c45f086.herokuapp.com",
    "https://davi-fss.github.io"
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
vehicle_controller = VehicleController()
point_controller = PointController()

# USER ENDPOINTS
@app.post("/user/create",status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser):
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

@app.get("/user/by-email", status_code=status.HTTP_200_OK)
async def read_user_by_email(email: str):
    user = user_controller.read_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@app.get("/user/by-id/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int):
    user = user_controller.read_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@app.get("/user/get-all-drivers", status_code=status.HTTP_200_OK)
async def read_all_drivers():
    user = user_controller.read_all_drivers()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@app.get("/user/get-drivers-without-vehicle", status_code=status.HTTP_200_OK)
async def read_drivers_without_vehicle():
    user = user_controller.read_drivers_without_vehicle()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@app.put("/user/update",status_code=status.HTTP_200_OK)
async def update_user(user: UpdateUser):
    try:
        return user_controller.update_user(user)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.delete("/user/delete",status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    try:
        return user_controller.delete_user(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/user/details",status_code=status.HTTP_200_OK)
async def user_details(user_id: int):
    try:
        return user_controller.user_details(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

# USER_TYPE ENDPOINT
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
    
@app.get("/user-phone/get-by-user", status_code=status.HTTP_200_OK)
async def get_phone_by_user_id(user_id: int):
    try:
        return user_phone_controller.get_phone_by_user_id(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
# STUDENT ENDPOINTS
@app.post("/student/create-list",status_code=status.HTTP_201_CREATED)
async def create_student(student_list: List[CreateStudent]):
    try:
        return student_controller.create_student_list(student_list=student_list)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.put("/student/update", status_code=status.HTTP_200_OK)
async def update_student(student: UpdateStudent):
    try:
        return student_controller.update_student(student=student)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.delete("/student/delete", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int):
    try:
        return student_controller.delete_student(student_id=student_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/student/get-by-responsible", status_code=status.HTTP_200_OK)
async def get_students_by_responsible(responsible_id: int):
    try:
        students = student_controller.get_students_by_responsible(responsible_id=responsible_id)

        if(len(students) == 0):
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Sem alunos cadastrados")
        
        return students
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/student/get-by-code", status_code=status.HTTP_200_OK)
async def get_student_by_code(student_code: str):
    try:
        return student_controller.get_student_by_code(student_code)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.post("/student/association", status_code=status.HTTP_200_OK)
async def create_student_association(association: StudentAssociation):
    try:
        return student_controller.create_association_student_responsible(association)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
# VEHICLE ENDPOINTS
@app.get("/vehicle/get-all",status_code=status.HTTP_200_OK)
async def get_all_vehicle():
    try:
        return vehicle_controller.get_all_vehicle()
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.post("/vehicle/create",status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle: CreateVehicle):
    try:
        return vehicle_controller.create_vehicle(vehicle)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/vehicle/update",status_code=status.HTTP_200_OK)
async def update_vehicle(vehicle: UpdateVehicle):
    try:
        return vehicle_controller.update_vehicle(vehicle)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.delete("/vehicle/delete",status_code=status.HTTP_200_OK)
async def delete_vehicle(vehicle_id: int):
    try:
        return vehicle_controller.delete_vehicle(vehicle_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/vehicle/get-by-driver",status_code=status.HTTP_200_OK)
async def get_vehicle_by_driver(user_id: int):
    try:
        vehicle = vehicle_controller.get_vehicle_by_driver(user_id)

        if(vehicle is None):
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Sem veículo cadastrado")

        return vehicle
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
#POINT ENDPOINTS
@app.get("/point/get-by-id",status_code=status.HTTP_200_OK)
async def get_point_by_id(point_id: int):
    try:
        return point_controller.get_point_by_id(point_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/point/get-by-user",status_code=status.HTTP_200_OK)
async def get_by_user(user_id: int):
    try:
        return point_controller.get_point_by_user_id(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.post("/point/create",status_code=status.HTTP_201_CREATED)
async def create_point(point: CreatePoint):
    try:
        return point_controller.create_point(point)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.post("/point/school-driver-association",status_code=status.HTTP_201_CREATED)
async def create_driver_association(association: DriverAssociation):
    try:
        return point_controller.create_driver_point_association(association)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/point/update",status_code=status.HTTP_200_OK)
async def update_point(point: UpdatePoint):
    try:
        return point_controller.update_point(point)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.delete("/point/delete",status_code=status.HTTP_200_OK)
async def delete_point(point_id: int):
    try:
        return point_controller.delete_point(point_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/point/get-all-schools-list",status_code=status.HTTP_200_OK)
async def get_school_list():
    try:
        school_list = point_controller.get_all_school_list()

        if(school_list is None):
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Sem escola cadastrada")

        return school_list
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))