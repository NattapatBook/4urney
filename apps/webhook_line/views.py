from http.client import responses
import os
from uu import decode

import requests
import time
import json
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.bot.utils import call_bot

from apps.webhook_line.connector import get_username, reply_message
from apps.webhook_line.verification import verify_line_signature
from apps.webhook_line.models import LineIntegration

LINE_CHATBOT_API_KEY = os.environ.get('LINE_CHATBOT_API_KEY')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

# Create your views here.
@csrf_exempt
async def webhook(request: HttpRequest, uuid):
    print(uuid)
    line_integration = LineIntegration.objects.get(uuid=uuid)
    LINE_CHATBOT_API_KEY = line_integration.line_chatbot_api_key
    LINE_CHANNEL_SECRET = line_integration.line_channel_secret
    organization_id = line_integration.organization_id

    print(request.headers)
    try:
        assert request.method == 'POST'
        body = request.body
        data = json.loads(body.decode('utf-8'))
        assert verify_line_signature(body, request.headers['X-Line-Signature'], LINE_CHANNEL_SECRET)
    except:
        data = None

    if data:
        print(data)
        event = data['events'][0]
        user_id = event['source']['userId']
        message_type = event['message']['type']
        reply_token = event['replyToken']

        if message_type == "text":
            """
            If user response as text
            """
            message = event['message']["text"]
            message_dt = event['timestamp']


            # response = requests.post(model_url_post,
            #                          json={"user_id": user_id, "username": username, "message_type": message_type,
            #                                "msg": message, "message_dt": message_dt, "reply_token": reply_token})
            #
            # print(response)

            #TODO query 5 latest message

            responses_message = call_bot(message)

            if responses_message:
                await reply_message(user_id,reply_token,responses_message,LINE_CHATBOT_API_KEY)
            else:
                print("Bot is not response due to agent's open ticket.")
        elif message_type == 'image':
            """
            If user responseg as image
            """
            # image_url = payload.events[0].message["contentProvider"].originalContentUrl
            # message = HumanMessage(
            #     content=[
            #         {
            #             "type": "text",
            #             "text": "What's in this image?",
            #         },  # You can optionally provide text parts
            #         {"type": "image_url", "image_url": image_url},
            #     ]
            # )
            # reply_message = llm_vision.invoke([message])
            # print(reply_message)
            await reply_message(user_id, reply_token,
                               "ขออภัยด้วยค่ะ ฉันไม่สามารถเข้าใจภาพที่คุณส่งมา กรุณาส่งเป็นข้อความแทนนะคะ",
                               LINE_CHATBOT_API_KEY)  # Insert Channel access token
        elif message_type == 'sticker':
            """
            If user response as sticker
            """
            # image_url = payload.events[0].message["contentProvider"].originalContentUrl
            # message = HumanMessage(
            #     content=[
            #         {
            #             "type": "text",
            #             "text": "What's in this image?",
            #         },  # You can optionally provide text parts
            #         {"type": "image_url", "image_url": image_url},
            #     ]
            # )
            # reply_message = llm_vision.invoke([message])
            # print(reply_message)
            await reply_message(user_id, reply_token,
                               "ขออภัยด้วยค่ะ ฉันไม่สามารถเข้าใจ sticker ที่คุณส่งมา กรุณาส่งเป็นข้อความแทนนะคะ",
                               LINE_CHATBOT_API_KEY)  # Insert Channel access token

    response = HttpResponse('')
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response