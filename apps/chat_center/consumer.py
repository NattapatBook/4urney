from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from psycopg2 import connect

from apps.chat_center.models import OrganizationMember
from models import Organization, Message, Customer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # self.channel_name
        # self.channel_layer
        # self.group_name = 'hello'
        # await self.channel_layer.group_add(self.group_name, self.channel_name)
        # await self.accept()

        # self.scope['user']

        self.scope['user']
        membership = OrganizationMember.objects.filter(user=self.scope['user']).first()
        # เก็ย orgs ไว้ใน session กรณีหลาย orgs

        if membership:
            # self.organization_id = membership.organization_id
            self.group_name = membership.organization_id
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.accept()
            await self.close()

    async def receive_json(self, content, **kwargs):
        # await self.channel_layer.group_send(self.group_name, {
        #     'type': 'send_json',
        #     'event': content,
        # })

        message = content.get('message')
        room_id = content.get('room_id')

        if not message or not room_id:
            return

        #TODO คนส่งกับคนรับอยู่ org เดียวกันไหม
        await database_sync_to_async(self.create_message)(
            platform_id=room_id,
            message=message,
            organization_id=self.organization_id
        )

        await self.channel_layer.group_send(self.group_name, {
            'type': 'send_json',
            'event': content,
        })

    def create_message(self, platform_id, message, organization_id):
        try:
            customer = Customer.objects.get(platform_id=platform_id)
        except Customer.DoesNotExist:
            return

        Message.objects.create(
            platform_id=platform_id,
            message=message,
            by='admin',
            timestamp=datetime.now(),
            organization_id=organization_id
        )

# TestDataConsumer สำหรับการส่งข้อมูลทดสอบ
import json
from datetime import datetime
class TestDataConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # เชื่อมต่อ WebSocket
        await self.accept()

    async def receive(self, text_data):
        # รับข้อความจาก WebSocket
        data = json.loads(text_data)
        
        # ตรวจสอบว่าเป็นคำขอสำหรับข้อมูลหรือไม่
        if data.get('type') == 'fetch_test_data':
            # ข้อมูลที่ต้องการส่งกลับ
            testArr = [
                {
                    "id": "-1", 
                    "img": "",
                    "name": "test", 
                    "tag": "", 
                    "priority": "",
                    "lastestMsg": "test_lastest_msg", 
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S+0700'),
                    "isUrgent": False,
                    "provider": "tiktok", 
                    "agent": "Me",
                    "messageType": "Opened Messages",
                    "replyToken": "-1"
                }
            ]

            # ส่งข้อมูลกลับไปยัง WebSocket
            await self.send(text_data=json.dumps({
                'type': 'test_data',
                'data': testArr
            }))