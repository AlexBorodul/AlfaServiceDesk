"""
ASGI config for service_desk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from tickets.consumer import ServiceDeskConsumer
from django.core.asgi import get_asgi_application
from django.urls import path
import sys
import os

sys.path.append('/root/AlfaServiceDesk')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service_desk.settings")

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws', ServiceDeskConsumer.as_asgi())
        ])
    )
})
print(application)
