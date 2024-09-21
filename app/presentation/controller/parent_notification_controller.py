from presentation.dto.CreateParentNotification import CreateParentNotification
from business.service.parent_notification_service import ParentNotificationService

class ParentNotificationController():
    parent_notification_service: ParentNotificationService

    def __init__(self):
        self.parent_notification_service = ParentNotificationService()

    def create_parent_notification(self, notification: CreateParentNotification):
        self.parent_notification_service.create_parent_notification(notification)