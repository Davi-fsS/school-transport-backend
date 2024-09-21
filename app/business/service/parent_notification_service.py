from data.repository.user_point_repository import UserPointRepository
from data.repository.point_repository import PointRepository
from data.repository.student_repository import StudentRepository
from data.repository.user_repository import UserRepository
from data.model.parent_notification_model import ParentNotificationModel
from presentation.dto.CreateParentNotification import CreateParentNotification
from data.repository.parent_notification_repository import ParentNotificationRepository

class ParentNotificationService():
    parent_notification_repository: ParentNotificationRepository
    user_repository: UserRepository
    student_repository: StudentRepository
    point_repository: PointRepository
    user_point_repository: UserPointRepository

    def __init__(self):
        self.parent_notification_repository = ParentNotificationRepository()
        self.user_repository = UserRepository()
        self.student_repository = StudentRepository()
        self.point_repository = PointRepository()
        self.user_point_repository = UserPointRepository()

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

        parent_notification_model = ParentNotificationModel(user_id = notification.user_id, student_id = notification.student_id,
                                                            inative_day = notification.inative_day, parent_notification_period_id = notification.period_id)

        self.parent_notification_repository.create_notification(parent_notification_model)