from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from threading import Thread
import time
import requests
import random
import os
import json
from asgiref.sync import async_to_sync, sync_to_async

from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class K8SStreamThread(Thread):
    def __init__(self, websocket, name, message):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = name
        self._running = True
        self.message = message

    def terminate(self):
        print("terminating")
        self._running = False

    def run(self):
        if not self._running:
            return
        while self._running:
            print(self._running)
            time.sleep(1)
            res = random.randint(1, 10)
            async_to_sync(channel_layer.send)(
                self.stream,
                {
                    'type': 'log_send',
                    'message': f"======{self.message}=========="
                }
            )


class SSHConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.kub_stream = None

        await self.accept()

    async def disconnect(self, close_code):
        self.kub_stream.terminate()
        self.kub_stream.join()
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        if self.kub_stream:
            self.kub_stream.terminate()
            self.kub_stream.join()
            time.sleep(2)
        self.kub_stream = K8SStreamThread(self, self.channel_name,message)
        self.kub_stream.daemon = True
        self.kub_stream.start()


    async def log_send(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
