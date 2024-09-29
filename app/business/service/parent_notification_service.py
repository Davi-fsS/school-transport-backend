from typing import List
from data.repository.parent_notification_period_repository import ParentNotificationPeriodRepository
from presentation.dto.Point import Point
from presentation.dto.Student import Student
from presentation.dto.ParentNotification import ParentNotification
from data.repository.user_point_repository import UserPointRepository
from data.repository.point_repository import PointRepository
from data.repository.student_repository import StudentRepository
from data.repository.user_repository import UserRepository
from data.model.parent_notification_model import ParentNotificationModel
from presentation.dto.CreateParentNotification import CreateParentNotification
from data.repository.parent_notification_repository import ParentNotificationRepository
from datetime import datetime, timedelta

class ParentNotificationService():
    parent_notification_repository: ParentNotificationRepository
    user_repository: UserRepository
    student_repository: StudentRepository
    point_repository: PointRepository
    user_point_repository: UserPointRepository
    parent_notification_period_repository: ParentNotificationPeriodRepository

    def __init__(self):
        self.parent_notification_repository = ParentNotificationRepository()
        self.user_repository = UserRepository()
        self.student_repository = StudentRepository()
        self.point_repository = PointRepository()
        self.user_point_repository = UserPointRepository()
        self.parent_notification_period_repository = ParentNotificationPeriodRepository()

    def create_parent_notification(self, notification: CreateParentNotification):
        user = self.user_repository.get_user(notification.user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        student = self.student_repository.get_student(notification.student_id)

        if student is None:
            raise ValueError("Aluno inválido")
        
        student_point = self.point_repository.get_point(student.point_id)

        if student_point is None:
            raise ValueError("Ponto inválido")
        
        if student_point.point_type_id == 2:
            raise ValueError("Ponto não é uma residência")

        user_point = self.user_point_repository.get_user_point_by_point(student_point.id)

        if user_point.user_id != user.id:
            raise ValueError("Este aluno não está no endereço deste responsável")
        
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        is_date_valid = notification.inative_day.date() >= tomorrow

        if not is_date_valid:
            raise ValueError("A data deve ser pelo menos 1 dia à frente da data atual.")

        parent_notification_model = ParentNotificationModel(user_id = notification.user_id, student_id = notification.student_id, point_id = student.point_id,
                                                            inative_day = notification.inative_day, parent_notification_period_id = notification.period_id,
                                                            creation_user=notification.user_id)

        self.parent_notification_repository.create_notification(parent_notification_model)

    def get_parent_notification_active_list_by_user(self, user_id: int):        
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        parent_notification_list = self.parent_notification_repository.get_notification_list_after_today_by_user(user.id)

        return self.get_parent_notification_list_dto(parent_notification_list)
    
    def get_parent_notification_past_list_by_user(self, user_id: int):        
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")
        
        past_parent_notification_list = self.parent_notification_repository.get_notification_list_past_by_user(user.id)

        canceled_parent_notification_list = self.parent_notification_repository.get_canceled_notification_list_by_user(user.id)

        return self.get_parent_notification_list_dto(past_parent_notification_list + canceled_parent_notification_list)
    
    def get_period_options(self):
        return self.parent_notification_period_repository.get_all()
    
    def put_period_disabled(self, id: int, user_id: int):
        user = self.user_repository.get_user(user_id)

        if user is None:
            raise ValueError("Usuário inválido")
        
        if user.user_type_id == 2:
            raise ValueError("Usuário não é um responsável")

        notification = self.parent_notification_repository.get_by_id(id)

        if notification is None:
            raise ValueError("Ocorrência inexistente")

        if notification.user_id != user.id:
            raise ValueError("Operação não autorizada")

        return self.parent_notification_repository.put_notification_disabled(id)
    
    def get_parent_notification_list_dto(self, parent_notification_list: List[ParentNotificationModel]):
        parent_notifications_dto : List[ParentNotification] = []

        point_list_dto : List[Point] = []
        student_list_dto : List[Student] = []

        parent_notification_period_all = self.parent_notification_period_repository.get_all()

        point_ids = []
        student_ids = []
        for parent_notification in parent_notification_list:
            point_ids.append(parent_notification.point_id)
            student_ids.append(parent_notification.student_id)

        point_list = self.point_repository.get_points_by_point_list(point_ids)

        student_list = self.student_repository.get_students_by_student_list(student_ids)

        for point in point_list:
            point_list_dto.append(Point(id=point.id, name=point.name, address=point.address,
                                        lat=point.lat, lng=point.lng, alt=point.alt, city=point.city,
                                        neighborhood=point.neighborhood, state=point.state,
                                        description=point.description, point_type_id=point.point_type_id))
        
        for student in student_list:
            student_list_dto.append(Student(id=student.id, name=student.name, year=student.year,
                                            code=student.code, point_id=student.point_id, creation_user=student.creation_user))

        for parent_notification in parent_notification_list:
            point_dto = list(filter(lambda p: p.id == parent_notification.point_id, point_list_dto))[0]
            student_dto = list(filter(lambda s: s.id == parent_notification.student_id, student_list_dto))[0]
            period_dto = list(filter(lambda p: p.id == parent_notification.parent_notification_period_id, parent_notification_period_all))[0]

            parent_notifications_dto.append(ParentNotification(home=point_dto, student=student_dto, id=parent_notification.id,
                                                               inative_day=parent_notification.inative_day,
                                                               period=period_dto.name, canceled=parent_notification.disabled))
            
        return parent_notifications_dto