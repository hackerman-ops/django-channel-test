from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from threading import Thread
import time
import requests
import random
import os
import json
from asgiref.sync import async_to_sync, sync_to_async


class K8SStreamThread(Thread):
    def __init__(self, websocket, name):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = name
        self._running = True

    def terminate(self):
        print("terminating")
        self._running = False

    def test(self):
        print("wpcal")

    def run(self):
        if not self._running:
            return
        while self._running:
            print(self._running)
            time.sleep(1)
            res = random.randint(1, 10)
            async_to_sync(self.websocket.send)(f"======{res}==========")


class SSHConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.name = self.scope["url_route"]["kwargs"]["name"]

        self.kub_stream = K8SStreamThread(self, self.name)

        self.kub_stream.daemon = True
        self.kub_stream.start()
        await self.accept()

    async def disconnect(self, close_code):
        self.kub_stream.terminate()
        self.kub_stream.join()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.send(message)
