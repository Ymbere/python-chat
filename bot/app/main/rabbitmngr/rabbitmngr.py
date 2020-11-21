import pika


class RabbitManager():
    def __init__(self):
        self.connection = None

    def init_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.connection = connection
        return connection
