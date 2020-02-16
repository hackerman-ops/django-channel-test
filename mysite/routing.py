# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from chat import consumers
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.urls import re_path

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
    }
)
