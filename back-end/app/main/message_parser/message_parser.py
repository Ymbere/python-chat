import json


class MessageParser():
    def prepere_message(self, response_body):
        full_response = {}
        response_converted = json.loads(response_body)
        full_response['data'] = response_converted['data']
        full_response['time'] = response_converted['time']
        full_response['owner'] = response_converted['owner']
        return full_response
