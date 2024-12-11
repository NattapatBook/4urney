import traceback
from importlib import import_module

from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from django.urls import re_path
import os

def route_apps(apps_settings):
    routes = []

    for app_name in apps_settings:
        module_name = f'apps.{app_name}.routes'
        if os.path.exists(settings.BASE_DIR / (module_name.replace('.', '/') + '.py')):
            module = import_module(module_name)
        else:
            continue

        app_routes: list = getattr(module, 'routes', None)
        if not isinstance(app_routes, list):
            continue

        for suffix, consumer in app_routes:
            routes.append(re_path(f'ws/{app_name}/{suffix}', consumer.as_asgi()))
    return routes


class NotFoundConsumer(WebsocketConsumer):
    async def connect(self):
        self.close()


websocket_urlpatterns = [
    *route_apps(settings.PROJECT_APPS),
    re_path(r".*", NotFoundConsumer.as_asgi()),
]
