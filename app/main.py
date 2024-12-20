from fastapi import FastAPI, Request, status, HTTPException, Header
from presentation.dto.SaveLoraCoordinate import SaveLoraCoordinate
from presentation.dto.UpdateDevice import UpdateDevice
from presentation.dto.CreateDevice import CreateDevice
from presentation.controller.device_controller import DeviceController
from presentation.dto.CreateParentNotification import CreateParentNotification
from presentation.dto.GetHistoricByDate import GetHistoricByDate
from presentation.controller.parent_notification_controller import ParentNotificationController
from presentation.dto.ScheduleStudentPosition import ScheduleStudentPosition
from presentation.dto.PutSchedulePoint import PutSchedulePoint
from presentation.dto.EndSchedule import EndSchedule
from presentation.dto.UpdateStudentAddress import UpdateStudentAddress
from presentation.dto.StartSchedule import StartSchedule
from presentation.dto.UpdateVehiclePoint import UpdateVehiclePoint
from presentation.dto.CreateVehiclePoint import CreateVehiclePoint
from presentation.controller.vehicle_point_controller import VehiclePointController
from presentation.dto.VehiclePointAssociation import VehiclePointAssociation
from presentation.controller.schedule_controller import ScheduleController
from presentation.controller.coordinate_controller import CoordinateController
from presentation.controller.user_controller import UserController
from presentation.controller.user_point_controller import UserPointController
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
from presentation.dto.SaveCoordinate import SaveCoordinate
from presentation.dto.UpdatePoint import UpdatePoint
from presentation.dto.CreateSchedule import CreateSchedule
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from presentation.middleware.firebase_auth_middleware import FirebaseAuthMiddleware

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

# apenas localmente
# app.add_middleware(FirebaseAuthMiddleware)

user_controller = UserController()
user_type_controller = UserTypeController()
user_phone_controller = UserPhoneController()
student_controller = StudentController()
vehicle_controller = VehicleController()
point_controller = PointController()
coordinate_controller = CoordinateController()
schedule_controller = ScheduleController()
vehicle_point_controller = VehiclePointController()
user_point_controller = UserPointController()
parent_notification_controller = ParentNotificationController()
device_controller = DeviceController()

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
    
@app.get("/user/driver-details-by-code",status_code=status.HTTP_200_OK)
async def get_driver_detals_by_code(code: str):
    try:
        return user_controller.get_driver_detals_by_code(code)
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

@app.post("/student/create",status_code=status.HTTP_201_CREATED)
async def create_student(student: CreateStudent):
    try:
        return student_controller.create_student(student)
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
async def get_students_by_responsible(responsible_id: int, request: Request):
    try:
        students = student_controller.get_students_by_responsible(responsible_id=responsible_id)

        if(len(students) == 0):
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Sem alunos cadastrados")
        
        return students
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/student/get-by-point-responsible", status_code=status.HTTP_200_OK)
async def get_students_by_point_responsible(responsible_id: int):
    try:
        students = student_controller.get_students_by_point_responsible(responsible_id=responsible_id)

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
    
@app.get("/student/details", status_code=status.HTTP_200_OK)
async def get_student_details(student_id: int):
    try:
        return student_controller.get_student_details(student_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.post("/student/association", status_code=status.HTTP_200_OK)
async def create_student_association(association: StudentAssociation):
    try:
        return student_controller.create_association_student_responsible(association)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.post("/student/disassociation", status_code=status.HTTP_200_OK)
async def student_disassociation(disassociation: StudentAssociation):
    try:
        return student_controller.disassociation_student_responsible(disassociation)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/student/update-address", status_code=status.HTTP_200_OK)
async def update_student_address(body: UpdateStudentAddress):
    try:
        return student_controller.update_student_address(body.student_id, body.user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/student/update-address-by-point", status_code=status.HTTP_200_OK)
async def update_student_address(body: UpdateStudentAddress):
    try:
        return student_controller.update_student_address_by_point_id(body.student_id, body.user_id, body.point_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/student/list-all-homes", status_code=status.HTTP_200_OK)
async def get_all_student_homes(student_id: int = Header(), user_id: int = Header()):
    try:
        return student_controller.get_all_student_homes(student_id, user_id)
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

@app.get("/vehicle/get-list-by-driver",status_code=status.HTTP_200_OK)
async def get_vehicle_list_by_driver(user_id: int):
    try:
        vehicle = vehicle_controller.get_vehicle_list_by_driver(user_id)

        if(vehicle is None):
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Sem veículo cadastrado")

        return vehicle
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/vehicle/associate-point",status_code=status.HTTP_200_OK)
async def vehicle_association_point(association: VehiclePointAssociation):
    try:
        return vehicle_controller.vehicle_association_point(association)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/vehicle/disassociate-point",status_code=status.HTTP_200_OK)
async def vehicle_disassociation_point(disassociation: VehiclePointAssociation):
    try:
        return vehicle_controller.vehicle_disassociation_point(disassociation)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

#USER_POINT ENDPOINTS
@app.get("/user-point/driver-school-by-code",status_code=status.HTTP_200_OK)
async def get_driver_school_by_code(code: str):
    try:
        return user_point_controller.get_driver_school_by_code(code)
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
    
@app.get("/point/get-school-by-user",status_code=status.HTTP_200_OK)
async def get_school(user_id: int):
    try:
        return point_controller.get_school_by_user(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/point/get-school-associated-by-driver",status_code=status.HTTP_200_OK)
async def get_school_associated_by_driver(user_id: int):
    try:
        return point_controller.get_school_associated_by_driver(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/point/get-school-by-driver",status_code=status.HTTP_200_OK)
async def get_school_by_driver(user_id: int):
    try:
        return point_controller.get_school_by_driver(user_id)
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

@app.delete("/point/school-driver-disassociation",status_code=status.HTTP_200_OK)
async def delete_driver_association(disassociation: DriverAssociation):
    try:
        return point_controller.delete_driver_point_association(disassociation)
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

#COORDINATE ENDPOINTS
@app.post("/coordinate/save-coordinates-mobile",status_code=status.HTTP_201_CREATED)
async def save_coordinates_mobile(coordinates: SaveCoordinate):
    try:
        return coordinate_controller.save_coordinate_mobile(coordinates)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/coordinate/get-by-schedule",status_code=status.HTTP_200_OK)
async def get_coordinates_by_schedule(schedule_id: int):
    try:
        return coordinate_controller.get_coordinates_by_schedule(schedule_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/coordinate/get-last-position-by-schedule",status_code=status.HTTP_200_OK)
async def get_last_coordinate_by_schedule(schedule_id : int = Header(), user_id : int = Header()):
    try:
        return coordinate_controller.get_last_coordinate_by_schedule(schedule_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.post("/coordinate/save-coordinates-lora",status_code=status.HTTP_201_CREATED)
async def save_coordinates_lora(coordinates: SaveLoraCoordinate):
    try:
        return coordinate_controller.save_coordinate_lora(coordinates)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

#SCHEDULE ENDPOINTS
@app.get("/schedule/by-student", status_code=status.HTTP_200_OK)
async def get_schedule_by_student(student_id: int = Header(), user_id: int = Header()):
    try:
        return schedule_controller.get_schedule_by_student(student_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/schedule/current-driver-details",status_code=status.HTTP_200_OK)
async def get_schedule_details_driver(schedule_id: int):
    try:
        return schedule_controller.get_driver_schedule_details_by_schedule_id(schedule_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/schedule/current-responsible-details",status_code=status.HTTP_200_OK)
async def get_schedule_details_responsible(schedule_id: int = Header(), user_id: int = Header()):
    try:
        return schedule_controller.get_responsible_schedule_details_by_schedule_id(schedule_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/schedule/get-current-schedules-by-user",status_code=status.HTTP_200_OK)
async def get_schedule_by_user(user_id: int):
    try:
        return schedule_controller.get_schedule_by_user(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/schedule/get-current-schedules-by-driver",status_code=status.HTTP_200_OK)
async def get_schedule_by_driver(user_id: int):
    try:
        return schedule_controller.get_schedule_by_driver(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.post("/schedule/create",status_code=status.HTTP_201_CREATED)
async def create_schedule(schedule: CreateSchedule):
    try:
        return schedule_controller.create_schedule(schedule)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/schedule/start",status_code=status.HTTP_200_OK)
async def put_schedule_start(start: StartSchedule):
    try:
        return schedule_controller.put_schedule_start(start)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.put("/schedule/point",status_code=status.HTTP_200_OK)
async def put_schedule_point(schedule_point: PutSchedulePoint):
    try:
        return schedule_controller.put_schedule_point(schedule_point)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.put("/schedule/end",status_code=status.HTTP_200_OK)
async def put_schedule_end(end: EndSchedule):
    try:
        return schedule_controller.put_schedule_end(end.schedule_id, end.user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/schedule/get-maps-infos",status_code=status.HTTP_200_OK)
async def get_schedule_maps_infos(schedule_id : int = Header(), user_id : int = Header()):
    try:
        return schedule_controller.get_schedule_maps_infos(schedule_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/schedule/get-student-position",status_code=status.HTTP_200_OK)
async def get_schedule_student_position(schedule_id : int = Header(), user_id : int = Header()):
    try:
        return schedule_controller.get_schedule_student_position(schedule_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.post("/schedule/get-driver-historic-by-date",status_code=status.HTTP_200_OK)
async def get_schedule_driver_historic_by_date(body: GetHistoricByDate):
    try:
        return schedule_controller.get_schedule_driver_historic_by_date(body.date, body.user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/schedule/get-driver-historic-details",status_code=status.HTTP_200_OK)
async def get_schedule_driver_historic_details(schedule_id : int = Header(), user_id : int = Header()):
    try:
        return schedule_controller.get_schedule_driver_historic_details(schedule_id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.post("/schedule/get-responsible-historic-by-date",status_code=status.HTTP_200_OK)
async def get_schedule_responsible_historic_by_date(body: GetHistoricByDate):
    try:
        return schedule_controller.get_schedule_responsible_historic_by_date(body.date, body.user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@app.get("/schedule/get-responsible-historic-details",status_code=status.HTTP_200_OK)
async def get_schedule_responsible_historic_details(schedule_id : int = Header(), user_id : int = Header(), point_id : int = Header()):
    try:
        return schedule_controller.get_schedule_responsible_historic_details(schedule_id, user_id, point_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
   
# PARENT_NOTIFICATION ENDPOINTS
@app.post("/parent_notification/create",status_code=status.HTTP_201_CREATED)
async def create_parent_notification(notification: CreateParentNotification):
    try:
        return parent_notification_controller.create_parent_notification(notification)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/parent_notification/get-active-list-by-user",status_code=status.HTTP_200_OK)
async def get_parent_notification_active_list_by_user(user_id: int):
    try:
        return parent_notification_controller.get_parent_notification_active_list_by_user(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/parent_notification/get-past-list-by-user",status_code=status.HTTP_200_OK)
async def get_parent_notification_past_list_by_user(user_id: int):
    try:
        return parent_notification_controller.get_parent_notification_past_list_by_user(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/parent_notification/get-period-options",status_code=status.HTTP_200_OK)
async def get_period_options():
    try:
        return parent_notification_controller.get_period_options()
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.put("/parent_notification/cancel-by-id",status_code=status.HTTP_200_OK)
async def put_period_disabled(id: int = Header(), user_id : int = Header()):
    try:
        return parent_notification_controller.put_period_disabled(id, user_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
# DEVICE ENDPOINTS
@app.post("/device/create",status_code=status.HTTP_200_OK)
async def create_device(device: CreateDevice):
    try:
        return device_controller.create_device(device)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.get("/device/get-all",status_code=status.HTTP_200_OK)
async def get_all_device():
    try:
        return device_controller.get_all_device()
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.put("/device/update",status_code=status.HTTP_200_OK)
async def update_device(device: UpdateDevice):
    try:
        return device_controller.update_device(device)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

@app.delete("/device/delete",status_code=status.HTTP_200_OK)
async def delete_device(id: int):
    try:
        return device_controller.delete_device(id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))