from http.client import responses
import os
from uu import decode

from datetime import datetime
import pytz
import requests
import time
import json
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from langsmith import Client
from asgiref.sync import sync_to_async

from apps.bot.chatbot_utils import call_bot, set_anonymizer
from apps.bot.connection_utils import execute_script, execute_to_df

from apps.webhook_line.connector import get_username, reply_message
from apps.webhook_line.verification import verify_line_signature
from apps.webhook_line.models import LineIntegration
from apps.chat_center.models import Message, Customer, Organization

MILVUS_COLLECTION_NAME_DRONE = os.environ.get('MILVUS_COLLECTION_NAME_DRONE')
MILVUS_URI=os.environ.get('MILVUS_URI')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
EMBEDDING_MODEL_API=os.environ.get('EMBEDDING_MODEL_API')
LANGCHAIN_TRACING_V2=os.environ.get('LANGCHAIN_TRACING_V2')
LANGCHAIN_ENDPOINT=os.environ.get('LANGCHAIN_ENDPOINT')
LANGCHAIN_API_KEY=os.environ.get('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT=os.environ.get('LANGCHAIN_PROJECT')

# Create your views here.
@csrf_exempt
async def webhook(request: HttpRequest, uuid):
    line_integration = await sync_to_async(LineIntegration.objects.get)(uuid=uuid)
    LINE_CHATBOT_API_KEY = line_integration.line_chatbot_api_key
    LINE_CHANNEL_SECRET = line_integration.line_channel_secret
    
    organization_id = line_integration.organization_id
    organization = await sync_to_async(Organization.objects.get)(id=organization_id)
    
    client = Client(anonymizer=set_anonymizer())
    
    # print(request.headers)
    try:
        assert request.method == 'POST'
        body = request.body
        data = json.loads(body.decode('utf-8'))
        assert verify_line_signature(body, request.headers['X-Line-Signature'], LINE_CHANNEL_SECRET)
    except:
        data = None

    if data:
        # print(data)
        event = data['events'][0]
        user_id = event['source']['userId']
        message_type = event['message']['type']
        reply_token = event['replyToken']
        username = get_username(user_id, LINE_CHATBOT_API_KEY)
        
        latest_messages = await sync_to_async(list)(Message.objects.filter(platform_id=user_id).all().order_by('-timestamp')[:10])
        
        # Output the messages
        chat_history = ""
        for message in latest_messages:
            chat_history += f"{message.by}: {message.message}" + '\n'
        
        df_routing_config = execute_to_df(f"""SELECT * FROM "4urney".routing_chain WHERE project_name = '{MILVUS_COLLECTION_NAME_DRONE}';""")
        
        df_user = execute_to_df(f"""SELECT * FROM "4urney".users WHERE id = '{user_id}';""")
        
        if df_user['messageType'].values != 'Opened Messages' or df_user.empty:

            if message_type == "text":
                """
                If user response as text
                """
                message = event['message']["text"]
                message_dt = event['timestamp']
                
                model_response = requests.post(EMBEDDING_MODEL_API, json = {"msg": message, "milvus_collection": MILVUS_COLLECTION_NAME_DRONE})
                
                retrieval_text = model_response.json()['retrieval_text']
                routing = model_response.json()['routing']

                responses_message = call_bot(chat_history=chat_history, routing=routing, message=message, retrieval_text=retrieval_text, df_routing_config=df_routing_config)
                responses_message = responses_message.content
                
                if responses_message:
                    await reply_message(user_id,reply_token,responses_message,LINE_CHATBOT_API_KEY)
                else:
                    print("Bot is not response due to agent's open ticket.")
                    
            elif message_type == 'image':
                """
                If user responseg as image
                """
                await reply_message(user_id, reply_token,
                                "ขออภัยด้วยค่ะ ฉันไม่สามารถเข้าใจภาพที่คุณส่งมา กรุณาส่งเป็นข้อความแทนนะคะ",
                                LINE_CHATBOT_API_KEY)  # Insert Channel access token
            elif message_type == 'sticker':
                """
                If user response as sticker
                """
                await reply_message(user_id, reply_token,
                                "ขออภัยด้วยค่ะ ฉันไม่สามารถเข้าใจ sticker ที่คุณส่งมา กรุณาส่งเป็นข้อความแทนนะคะ",
                                LINE_CHATBOT_API_KEY)  # Insert Channel access token
                
        else: 
            print("Admin is already Open Messaged with the customer.")
 
    new_customer = await sync_to_async(Customer.objects.update_or_create)(
        platform_id=user_id, 
        defaults = {
            'name':username, 
            'lastest_msg':message, 
            'timestamp':datetime.now(pytz.timezone('Asia/Bangkok')),
            'provider':'line', 
            'agent':'Me', 
            'message_type':'Closed Messages', 
            'reply_token':reply_token, 
            'organization_id':organization
        }
    )
    
    customer = await sync_to_async(Customer.objects.filter(platform_id=user_id).first)()
    if not customer:
        print(f"No Customer found with platform_id: {user_id}")
    
    user_new_message = await sync_to_async(Message.objects.create)(
        platform_id=customer,
        message=message,
        by='customer',
        # user=None,
        timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
        organization_id=organization,
    )
    
    bot_new_message = await sync_to_async(Message.objects.create)(
        platform_id=customer,
        message=responses_message,
        by='bot',
        # user=user,
        timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
        organization_id=organization,
    )
    
    response = HttpResponse('')
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    return response