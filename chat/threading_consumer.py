from channels.generic.websocket import WebsocketConsumer
from threading import Thread
import time
import requests
import random
import os

class K8SStreamThread(Thread):
    def __init__(self, websocket, name):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = name
        self._running = True

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
            self.websocket.send(f"======{res}==========")





class SSHConsumer(WebsocketConsumer):
    def connect(self):
        self.name = self.scope["url_route"]["kwargs"]["name"]


        self.kub_stream = K8SStreamThread(self, self.name)

        self.kub_stream.daemon = True
        self.kub_stream.start()
        self.accept()

    def disconnect(self, close_code):
        self.kub_stream.terminate()
        self.kub_stream.join()


    def receive(self, text_data):
        print("heh")