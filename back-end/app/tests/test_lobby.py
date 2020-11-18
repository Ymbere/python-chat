import json
from threading import Lock

import pika
from flask import Flask
from flask_socketio import SocketIO

from ..main.message_parser import MessageParser
from ..main.rabbitmngr import RabbitManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

thread = None
stop_thread = True
thread_lock = Lock()


def background_rabbit_consumer():
    count = 0
    while True:
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
        body=json.dumps({"data": "A new user as connected",
                         "time": "now", "owner": "system"})
    )
    rabbit_connection.close()

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_rabbit_consumer)


class TestLobby:
    def test_connection(self):
        client = socketio.test_client(app)
        client.connect('/lobby')
        assert client.is_connected() is True

        client2 = socketio.test_client(app)
        client2.connect('/lobby')
        assert client2.is_connected() is True

        socketio.sleep(10)

        received = client2.get_received('/lobby')
        assert len(received) == 2
        assert len(received[0]['args']) == 1
        assert received[0]['name'] == 'lobby_consumer'
        assert received[0]['args'][0]['data'] == 'A new user as connected'
        assert received[0]['args'][0]['time'] == 'now'
        assert received[0]['args'][0]['owner'] == 'system'

        received = client.get_received('/lobby')
        assert len(received) == 2
        assert len(received[0]['args']) == 1
        assert received[1]['name'] == 'lobby_consumer'
        assert received[1]['args'][0]['data'] == 'A new user as connected'
        assert received[1]['args'][0]['time'] == 'now'
        assert received[1]['args'][0]['owner'] == 'system'

        client.disconnect()
        assert client.is_connected() is False

        client2.disconnect()
        assert client2.is_connected() is False

    def test_on_lobby_consumer(self):
        client = socketio.test_client(app)
        client.connect('/lobby')

        client2 = socketio.test_client(app)
        client2.connect('/lobby')

        client.emit(
            'lobby_publisher',
            {'data': 'custom data', 'time': 'custom_time', 'owner': 'pytest'},
            namespace="/lobby"
        )

        socketio.sleep(2)

        received = client2.get_received('/lobby')
        assert len(received) == 2
        assert len(received[0]['args']) == 1
        assert received[1]['name'] == 'lobby_consumer'
        assert received[1]['args'][0]['data'] == 'custom data'
        assert received[1]['args'][0]['time'] == 'custom_time'
        assert received[1]['args'][0]['owner'] == 'pytest'
