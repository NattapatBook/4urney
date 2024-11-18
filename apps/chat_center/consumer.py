from channels.generic.websocket import AsyncJsonWebsocketConsumer
from psycopg2 import connect


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
