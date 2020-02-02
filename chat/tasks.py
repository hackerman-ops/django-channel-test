from celery import shared_task
import random
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
import os


@shared_task
def tailf(channel_name):
    channel_layer = get_channel_layer()

    try:

        while True:
            time.sleep(3)
            res = random.randint(1, 10)
            async_to_sync(channel_layer.send)(
                channel_name, {"type": "send.message", "message": "wtf" + str(res)}
            )

    except Exception as e:
        print(e)
