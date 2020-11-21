import json

import socketio
from datetime import datetime

from .main.api_fetcher import StockFetcher
from .main.rabbitmngr import RabbitManager

socketio_client = socketio.Client()
rabbit_manager = RabbitManager()
api_fetcher = StockFetcher()


class App():
    def run():
        socketio_client.connect('ws://127.0.0.1:5000', namespaces=['/lobby'])

    @socketio_client.on('connect', namespace='/lobby')
    def connect_to_chat():
        print("Connected to the chat, waiting for commands...")

    @socketio_client.on('lobby_consumer', namespace='/lobby')
    def lobby_consumer(data):
        message = data['data']
        rabbit_connection = rabbit_manager.init_connection()
        channel = rabbit_connection.channel()
        channel.queue_declare(queue='/lobby')

        if message.startswith('/'):
            stock_information = api_fetcher.fetch_stock_information(message)
            message = json.dumps(
                {
                    'data': stock_information,
                    'time': datetime.now().strftime("%H:%M"),
                    'owner': 'BOT'
                }
            )
            channel.basic_publish(
                exchange='',
                routing_key='/lobby',
                body=message
            )
            print(stock_information)

        print("message Received: ", data)
