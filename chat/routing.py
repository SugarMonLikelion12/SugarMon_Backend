from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chatRoom/<int:chatRoomId>', ChatConsumer.as_asgi()),
]