import pika
import json
import logging

from api.environment import Environment
from api.notification.service import Message, Notification
from api.notification.google import GoogleNotificationService

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

env = Environment.read()
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
    except Exception as e:
        import traceback
        LOG.error(f'error: {e}, trace: {traceback.format_exc()}')


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    connection_channel = connection.channel()
    connection_channel.exchange_declare(exchange='travel', exchange_type='topic')
    result = connection_channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    connection_channel.queue_bind(exchange='travel', queue=queue_name, routing_key='')
    LOG.info('[*] Waiting for messages. To exit press CTRL+C')
    connection_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    connection_channel.start_consuming()
