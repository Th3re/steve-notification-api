import json
import logging
import requests

from api.notification.service import NotificationService
from api.notification.service import Message, NotificationResponse

LOG = logging.getLogger(__name__)


class GoogleNotificationService(NotificationService):
    def __init__(self, token):
        self.token = token

    def send(self, topic: str, message: Message) -> NotificationResponse:
        body = {"to": f'/topics/{topic}',
                "notification": vars(message.notification)}
        response = requests.post('https://fcm.googleapis.com/fcm/send',
                                 headers={'Authorization': f'key={self.token}'},
                                 json=body)
        LOG.info(f'Google response: {response}')
        succeeded = 200 <= response.status_code < 300
        status = NotificationResponse.Status.OK if succeeded else NotificationResponse.Status.ERROR
        return NotificationResponse(response.json(), status)
