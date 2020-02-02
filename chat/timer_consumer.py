from channels.generic.websocket import WebsocketConsumer
from threading import Timer
import time
import requests
import random
import os


def time_send(websocket):

    res = random.randint(1, 10)
    websocket.send(f"======{res}==========")





class SSHConsumer(WebsocketConsumer):
    def connect(self):
        self.name = self.scope["url_route"]["kwargs"]["name"]


        self.kub_stream = Timer(interval=2,function=time_send,args=(self,))

        self.kub_stream.run()
        self.accept()

    def disconnect(self, close_code):
        self.kub_stream.cancel()



    def receive(self, text_data):
        print("heh")