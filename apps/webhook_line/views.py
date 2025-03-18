from channels.db import database_sync_to_async
import os
import pandas as pd
from datetime import datetime
import requests
import json, pytz

from channels.layers import get_channel_layer
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async

from langsmith import Client

from apps.bot.chatbot_utils import call_bot, set_anonymizer
from apps.bot.connection_utils import execute_to_df
from apps.bot.data_utils import extract_user_data

from apps.webhook_line.connector import get_username, reply_message
from apps.webhook_line.verification import verify_line_signature
from apps.webhook_line.models import LineIntegration, LineConnectionNew
from apps.chat_center.models import Message, Customer, Organization, RoutingChain, SkillConnection, FieldConnection, \
    InformationExtractionSkill, InformationExtractionSkillNew, RoutingSkill, OrganizationMember, CustomerNew, MessageNew

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
    client = Client(anonymizer=set_anonymizer())
    line_integration = await sync_to_async(LineIntegration.objects.get)(uuid=uuid)
    LINE_CHATBOT_API_KEY = line_integration.line_chatbot_api_key
    LINE_CHANNEL_SECRET = line_integration.line_channel_secret
    
    organization_id = line_integration.organization_id
    organization = await sync_to_async(Organization.objects.get)(id=organization_id)
    
    # print(request.headers)
    try:
        assert request.method == 'POST'
        body = request.body
        data = json.loads(body.decode('utf-8'))
        assert verify_line_signature(body, request.headers['X-Line-Signature'], LINE_CHANNEL_SECRET)
    except:
        data = None

    # @database_sync_to_async
    # def get_message_counts(organization):
    #     return list(
    #         MessageNew.objects.filter(by='bot', organization_id=organization)
    #         .values('organization_id')
    #         .annotate(message_count=Count('id'))
    #     )
        
    # message_counts = await get_message_counts(organization)
    
    # count_message = message_counts[0]['message_count']
    
    # if count_message >= 1:
    #     if data:
    #         event = data['events'][0]
    #         user_id = event['source']['userId']
    #         reply_token = event['replyToken']
    #         await reply_message(user_id, reply_token,
    #                             "ขออภัยด้วยค่ะ โควต้าบอทตอบหมด",
    #                             LINE_CHATBOT_API_KEY)
    #         customer_list = await get_customers()
    #         channel_layer = get_channel_layer()
    #         group_name = f'organization_{organization_id}'
    
    #         await channel_layer.group_send(
    #             group_name,
    #             {
    #                 'type': 'send_json_to_client',
    #                 'event': {
    #                     'id': user_id,
    #                     'type': 'message_update',
    #                     'formatted_data': customer_list
    #                 }
    #             }
    #         )
    
    #         response = HttpResponse('')
    #         response.headers["Access-Control-Allow-Origin"] = "*"
    
    #         return response

    if data:
        # print(data)
        event = data['events'][0]
        user_id = event['source']['userId']
        message_type = event['message']['type']
        reply_token = event['replyToken']
        message = event['message']["text"]
        message_dt = event['timestamp']
        username = get_username(user_id, LINE_CHATBOT_API_KEY) # บาสหมี
        
        # check if CustomerNew exists
        customer_new = await sync_to_async(CustomerNew.objects.filter(platform_id=user_id, from_line_uuid=line_integration).first)()
        customer_id = customer_new.id

        if customer_id:
            new_customer = await sync_to_async(CustomerNew.objects.update_or_create)(
                id = customer_id, 
                defaults = {
                    'name':username,
                    'platform_id':user_id, 
                    'lastest_msg':message,
                    'timestamp':datetime.now(pytz.timezone('Asia/Bangkok')),
                    'provider':'line',
                    'agent':'Me',
                    'message_type':'Closed Messages',
                    'reply_token':reply_token,
                    'organization_id':organization, 
                    'from_line_uuid': line_integration
                }
            )
        else: 
            # Add user before send message
            new_customer = await sync_to_async(CustomerNew.objects.create)(
                name=username,
                platform_id=user_id, 
                lastest_msg=message,
                timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
                provider='line',
                agent='Me',
                message_type='Closed Messages',
                reply_token=reply_token,
                organization_id=organization, 
                from_line_uuid=line_integration
            )

        latest_messages = await sync_to_async(list)(MessageNew.objects.filter(platform_id=customer_new).all().order_by('-timestamp')[:10])

        # Output the messages history
        chat_history = ""
        for history in latest_messages[::-1]:
            chat_history += f"{history.by}: {history.message}" + '\n'

        # get knowledge base (collection name) & routing candidates
        line_connection = await sync_to_async(lambda: list(LineConnectionNew.objects.filter(uuid=uuid).values_list('bot_id', flat=True)))()
        routing_configs = await sync_to_async(lambda: list(RoutingChain.objects.filter(id__in=line_connection).values()))()
        df_routing_config = pd.DataFrame(routing_configs)

        # get user config
        df_user = await sync_to_async(lambda: list(CustomerNew.objects.filter(id=customer_id).values()))()
        df_user = pd.DataFrame(df_user)

        if df_user['message_type'].values != 'Opened Messages' or df_user.empty:

            if message_type == "text":
                """
                If user response as text
                """
                model_response = requests.post(EMBEDDING_MODEL_API, json = {"msg": message, "milvus_collection": list(df_routing_config['knowledge_base']), "candidate_labels": list(df_routing_config['routing'])})

                try:
                    retrieval_text = model_response.json()['retrieval_text']
                    routing = model_response.json()['routing']
                except: 
                    print("No retrieval text were given. Use empty knowledge")
                    retrieval_text = ""
                    routing = ""
                

                responses_message = call_bot(chat_history=chat_history, routing=routing, message=message, retrieval_text=retrieval_text, df_routing_config=df_routing_config)
                responses_message = responses_message.content

                if responses_message:
                    await reply_message(user_id,reply_token,responses_message,LINE_CHATBOT_API_KEY)
                else:
                    print("Bot is not response due to agent's open ticket.")

            elif message_type == 'image':
                """
                If user response as image
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

    customer = await sync_to_async(CustomerNew.objects.filter(id=customer_id).first)()

    if not customer:
        print(f"No Customer found with platform_id: {user_id}")

    user_new_message = await sync_to_async(MessageNew.objects.create)(
        platform_id=customer,
        message=message,
        by='customer',
        # user=None,
        timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
        organization_id=organization,
        from_line_uuid=line_integration
    )

    bot_new_message = await sync_to_async(MessageNew.objects.create)(
        platform_id=customer,
        message=responses_message,
        by='bot',
        # user=user,
        timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
        organization_id=organization,
        from_line_uuid=line_integration
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

    # Add information extraction from bot
    message_object = await sync_to_async(MessageNew.objects.filter(platform_id=customer, message=message).order_by('-timestamp').first)()
    customer_object = await sync_to_async(CustomerNew.objects.filter(name=username, id=customer_id).first)()
    bot_ids = await sync_to_async(lambda: list(LineConnectionNew.objects.filter(uuid=line_integration).values_list("bot_id", flat=True)))()
    skill_ids = await sync_to_async(lambda: list(SkillConnection.objects.filter(bot_id__in=bot_ids).values_list("skill_id", flat=True)))()

    if skill_ids:
        field_names = await sync_to_async(lambda: list(FieldConnection.objects.filter(skill_id__in=skill_ids).values_list("field_name", flat=True)))()
        descriptions = await sync_to_async(lambda: list(FieldConnection.objects.filter(skill_id__in=skill_ids).values_list("field_description", flat=True)))()
        skill_response = extract_user_data(text=message, field_names=field_names, descriptions=descriptions)

    for (field_name, result), skill_id in zip(skill_response.items(), skill_ids):
        if result:
            field_connection = await sync_to_async(FieldConnection.objects.filter(field_name=field_name).first)()
            routing_skill = await sync_to_async(RoutingSkill.objects.filter(id=skill_id).first)()

            if field_connection:
                info_skill = InformationExtractionSkillNew(
                    field_id=field_connection,
                    field_name=field_name,
                    result=result,
                    skill_id=routing_skill,
                    user_id=customer_object,
                    message_id=message_object
                )

                await sync_to_async(info_skill.save)()

    response = HttpResponse('')
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response