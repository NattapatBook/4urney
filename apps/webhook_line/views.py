from channels.db import database_sync_to_async
import os

import pandas as pd
from datetime import datetime
import requests
import json, pytz

from channels.layers import get_channel_layer
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from langsmith import Client
from asgiref.sync import sync_to_async

from apps.bot.chatbot_utils import call_bot, set_anonymizer
from apps.bot.connection_utils import execute_to_df

from apps.webhook_line.connector import get_username, reply_message
from apps.webhook_line.verification import verify_line_signature
from apps.webhook_line.models import LineIntegration, RoutingChain
from apps.chat_center.models import Message, Customer, Organization

MILVUS_COLLECTION_NAME_DRONE = os.environ.get('MILVUS_COLLECTION_NAME_DRONE')
MILVUS_URI=os.environ.get('MILVUS_URI')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
EMBEDDING_MODEL_API=os.environ.get('EMBEDDING_MODEL_API')
LANGCHAIN_TRACING_V2=os.environ.get('LANGCHAIN_TRACING_V2')
LANGCHAIN_ENDPOINT=os.environ.get('LANGCHAIN_ENDPOINT')
LANGCHAIN_API_KEY=os.environ.get('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT=os.environ.get('LANGCHAIN_PROJECT')

tz = pytz.timezone('Asia/Bangkok')


@database_sync_to_async
def get_customers():
    customers = Customer.objects.all()
    customer_list = []
    for customer in customers:
        customer_data = {
            "id": customer.platform_id,
            "img": customer.img if customer.img else "",
            "name": customer.name if customer.name else "",
            "tag": customer.tag if customer.tag else "",
            "priority": customer.priority if customer.priority else "",
            "lastestMsg": customer.lastest_msg if customer.lastest_msg else "",
            "timestamp": customer.timestamp.astimezone(tz).strftime(
                "%Y-%m-%d %H:%M:%S%z") if customer.timestamp else "",
            "isUrgent": customer.is_urgent if customer.is_urgent is not None else False,
            "provider": customer.provider if customer.provider else "",
            "agent": customer.agent if customer.agent else "",
            "messageType": customer.message_type if customer.message_type else "",
            "replyToken": customer.reply_token if customer.reply_token else None
        }
        customer_list.append(customer_data)
    return customer_list

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
        
        # get routing config
        routing_configs = await sync_to_async(lambda: list(RoutingChain.objects.filter(knowledge_base=MILVUS_COLLECTION_NAME_DRONE).values()))()
        df_routing_config = pd.DataFrame(routing_configs)
        
        # get user config
        df_user = await sync_to_async(lambda: list(Customer.objects.filter(platform_id=user_id).values()))()
        df_user = pd.DataFrame(df_user)
        
        if df_user['message_type'].values != 'Opened Messages' or df_user.empty:

            if message_type == "text":
                """
                If user response as text
                """
                message = event['message']["text"]
                message_dt = event['timestamp']
                
                model_response = requests.post(EMBEDDING_MODEL_API, json = {"msg": message, "milvus_collection": MILVUS_COLLECTION_NAME_DRONE, "candidate_labels": list(df_routing_config['routing'])})

                retrieval_text = model_response.json()['retrieval_text']
                routing = model_response.json()['routing']

                responses_message = call_bot(chat_history=chat_history, routing=routing, message=message, retrieval_text=retrieval_text, df_routing_config=df_routing_config)
                responses_message = responses_message.content

                if responses_message:
                    await reply_message(user_id,reply_token,responses_message,LINE_CHATBOT_API_KEY)
                else:
                    print("Bot is not response due to agent's open ticket.")

                # responses_message = 'botja'
                # await reply_message(user_id,reply_token,responses_message,LINE_CHATBOT_API_KEY)

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

    customer_list = await get_customers()
    channel_layer = get_channel_layer()
    group_name = f'organization_{organization_id}'

    await channel_layer.group_send(
        group_name,
        {
            'type': 'send_json_to_client',
            'event': {
                'id': user_id,
                'type': 'message_update',
                'formatted_data': customer_list
            }
        }
    )

    response = HttpResponse('')
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    return response