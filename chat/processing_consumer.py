from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from threading import Thread
import time
import requests
import random
import os
from multiprocessing import Process
import subprocess
from asgiref.sync import async_to_sync,sync_to_async

from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()


def tailf(channel_name):

    while True:
        print("hh")
        time.sleep(3)
        res = random.randint(1,10)
        channel_layer.send(
            channel_name,
            {
                "type": "send.message",
                "message": "wtf" + str(res)
            }
        )




class SSHConsumer(WebsocketConsumer):
    def connect(self):
        self.name = self.scope["url_route"]["kwargs"]["name"]

        self.p = Process(target=tailf,args=(self.channel_name,))
        self.p.daemon = True
        self.p.run()
        self.accept()

    def disconnect(self, close_code):

        self.p.kill()
        print("killed")


    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))
