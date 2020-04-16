import pika
import json
import logging

from api.environment import read_environment
from api.notification.service import Message, Notification
from api.notification.google import GoogleNotificationService

LOG = logging.getLogger(__name__)

env = read_environment()
notification_service = GoogleNotificationService(env.google.apikey_fcm)


def callback(ch, method, properties, body):
    try:
        body = json.loads(body)
        location = body['event']['location']
        summary = body['event']['summary']
        start_time = body['event']['start_time']
        duration = body['travel']['duration'] // 60
        user_id = body['user_id']
        title = f'\'{summary}\' begins soon'
        subtitle = location
        body = f'Travel time is {duration} minutes'
        notification = Notification(title=title, subtitle=subtitle, body=body)
        message = Message(notification, body)
        notification_service.send(user_id, message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        import traceback
        LOG.error(f'error: {e}, trace: {traceback.format_exc()}')


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='travel', durable=True)
    LOG.info('[*] Waiting for messages')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='travel', on_message_callback=callback)
    channel.start_consuming()
