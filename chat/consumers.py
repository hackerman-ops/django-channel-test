# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import random
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        namespace = text_data_json["namespace"]
        pod = text_data_json["pod"]
        # Send message to room group
        print(namespace)
        print(pod)

        intmeaage = random.randint(1,10)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'log_send',
                'message': intmeaage
            }
        )

    # Receive message from room group
    async def log_send(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
