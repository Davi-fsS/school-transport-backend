from business.service.student_service import StudentService
from presentation.dto.CreateStudent import CreateStudent
import firebase_admin
from firebase_admin import credentials
from firebase_admin import app_check
import jwt
import os

class StudentController():
    student_service: StudentService
    firebase: any

    def __init__(self):
        cred_path = os.path.join(os.path.dirname(__file__), '../../../auth-firebase.json')
        cred=credentials.Certificate(cred_path)
        self.firebase = firebase_admin.initialize_app(cred)
        self.student_service = StudentService()
    
    def create_student(self, token: str, student: CreateStudent):
        try:
            app_check.verify_token(token=token)
            return self.student_service.create_student(student=student)
        except(app_check.InvalidTokenError, jwt.exceptions.DecodeError) as e:
            raise ValueError(str(e))