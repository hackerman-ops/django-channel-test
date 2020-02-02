# chat/routing.py
from django.urls import re_path

from . import consumers
from . import threading_consumer
from . import ay_processing_consumer
from . import processing_consumer
from . import timer_consumer
from . import ay_threading_consumer
from . import receive_ay_threading_consumer
from . import receiveagain_ay_threading_consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<name>\w+)/$', receiveagain_ay_threading_consumer.SSHConsumer),
    re_path(r'ws/thread/(?P<name>\w+)/$', threading_consumer.SSHConsumer),
    re_path(r'ws/timer/(?P<name>\w+)/$', timer_consumer.SSHConsumer),
    re_path(r'ws/aythread/(?P<name>\w+)/$', ay_threading_consumer.SSHConsumer),

]
