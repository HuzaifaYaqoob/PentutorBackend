import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentutor.settings')

django.setup()

import VideoChat.websockets.urls
from .websocket.SocketMiddlewares import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddleware(
        URLRouter(
            VideoChat.websockets.urls.websocket_urls
        )
    ),
})