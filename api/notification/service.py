import abc
import enum


class Notification:
    def __init__(self, title, subtitle, body):
        self.title = title
        self.subtitle = subtitle
        self.body = body


class Message:
    def __init__(self, notification, data):
        self.notification = notification
        self.data = data


class NotificationResponse:
    class Status(enum.Enum):
        OK = "OK"
        ERROR = "ERROR"

    def __init__(self, message: str, status: Status):
        self.message = message
        self.status = status


class NotificationService(abc.ABC):
    @abc.abstractmethod
    def send(self, topic: str, message: Message) -> NotificationResponse:
        pass
