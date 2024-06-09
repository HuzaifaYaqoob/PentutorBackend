"""
ASGI config for Pentutor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentutor.settings')
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application


# application = get_asgi_application()


import VideoChat.websockets.urls
from .websocket.SocketMiddlewares import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : TokenAuthMiddleware(
            URLRouter(
                VideoChat.websockets.urls.websocket_urls,
            )
        )

})