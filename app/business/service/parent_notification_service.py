from data.model.parent_notification_model import ParentNotificationModel
from presentation.dto.CreateParentNotification import CreateParentNotification
from data.repository.parent_notification_repository import ParentNotificationRepository

class ParentNotificationService():
    parent_notification_repository: ParentNotificationRepository

    def __init__(self):
        self.parent_notification_repository = ParentNotificationRepository()

    def create_parent_notification(self, notification: CreateParentNotification):

        parent_notification_model = ParentNotificationModel(user_id = notification.user_id)

        self.parent_notification_repository.create_notification(parent_notification_model)