"""
ASGI config for SugarMon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SugarMon.settings')

django_asgi_app = get_asgi_application()

applicaition = ProtocolTypeRouter({
    "http": django_asgi_app, # http 요청은 기존 방식을 채용
    "Websocket": AuthMiddleware(AllowedHostsOriginValidator( # ws 요청은 미들웨어 거친 후 chat.routing.py로 이동시킴
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ))
})
