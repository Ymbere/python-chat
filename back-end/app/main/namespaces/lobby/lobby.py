from flask_socketio import Namespace, emit
from threading import Lock
import pika
import json
from datetime import datetime

from pika.spec import BasicProperties
from ...rabbitmngr import RabbitManager
from ...message_parser import MessageParser
from .... import socketio

thread = None
stop_thread = 1
thread_lock = Lock()


def background_rabbit_consumer():
    count = 0
    while stop_thread:
        socketio.sleep(2)
        count += 1
        rabbit_connection = RabbitManager().init_connection()
        channel = rabbit_connection.channel()
        channel.queue_declare(queue='/lobby')

        def callback(ch, method, properties, body):
            body_decoded = body.decode()
            body_decoded = MessageParser().prepere_message(body_decoded)

            socketio.emit(
                'lobby_consumer',
                body_decoded,
                namespace='/lobby'
            )

        channel.basic_consume(
            queue='/lobby',
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()


@socketio.on('lobby_publisher', namespace='/lobby')
def on_lobby_publisher(message):
    message = json.dumps(message)

    rabbit_connection = RabbitManager().init_connection()
    channel = rabbit_connection.channel()
    channel.queue_declare(queue='/lobby')
    channel.basic_publish(
        exchange='',
        routing_key='/lobby',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )


@socketio.on('connect', namespace="/lobby")
def connected_lobby():

    rabbit_connection = RabbitManager().init_connection()
    channel = rabbit_connection.channel()
    channel.queue_declare(queue='/lobby')
    channel.basic_publish(
        exchange='',
        routing_key='/lobby',
        body=json.dumps(
            {
                "data": "A new user as connected",
                "time": datetime.now().strftime("%H:%M"),
                "owner": "system"
            }
        )
    )
    rabbit_connection.close()

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_rabbit_consumer)
