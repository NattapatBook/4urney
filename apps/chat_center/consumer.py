from channels.generic.websocket import AsyncJsonWebsocketConsumer
from psycopg2 import connect


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.channel_name
        self.channel_layer
        self.group_name = 'hello'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # self.scope['user']

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(self.group_name, {
            'type': 'send_json',
            'event': content,
        })

