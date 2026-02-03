from websockets.sync.client import connect
import json
from django_web.dam_site import settings


def send_message(message):
    print(message)
    print(json.dumps(message))
    with connect(settings.LLM_URL) as connection:
        connection.send(json.dumps(message))
        return connection.recv()