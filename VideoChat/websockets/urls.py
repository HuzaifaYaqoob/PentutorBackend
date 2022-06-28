
from django.urls import path

from .consumers.VideoChatConsumers import VideoChatConsumers

websocket_urls = [
    path('ws/video-chat/<str:videochat_id>/' , VideoChatConsumers.as_asgi() ),
]