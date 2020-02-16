# chat/routing.py
from django.urls import re_path

from . import tailf_changeprcess_consumer

websocket_urlpatterns = [
    re_path(r'ws/k8slog/(?P<stream>\w+)/$', tailf_changeprcess_consumer.tailflog),


]
