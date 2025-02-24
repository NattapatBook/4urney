import csv
import threading

from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404
from twisted.python.runtime import platform

from utils.function import short_uuid4
import os
import psycopg2
import json
import requests
import pytz
from datetime import datetime
import pandas as pd
from channels.layers import get_channel_layer
import asyncio
import boto3
from marshmallow.utils import timestamp

from rest_framework import status, permissions
from rest_framework.permissions import AllowAny

from apps.bot.chatbot_utils import call_bot
# from sympy import line_integrate

from apps.chat_center.models import User, OrganizationMember, Customer, Message, Dashboard, UploadedFile, RoutingChain, \
    ChatSummarize, ChatUserSatisfaction, ChatUserUrgent, InternalChatSession, InternalChatMessage, RequestDemo
from apps.webhook_line.models import LineIntegration, LineConnectionNew
from apps.webhook_line.connector import generate_access_key, connect_line_webhook
from apps.chat_center.serializers import FileUploadSerializer
from rest_framework.views import APIView
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
from apps.bot.function import *
from utility.function import *
from pymilvus import utility
from langchain.callbacks.tracers import LangChainTracer

DB_CONFIG = {
    'host': os.environ.get('DEMO_DATABASE_HOST'),
    'database': os.environ.get('DEMO_DATABASE_NAME'),
    'user': os.environ.get('DEMO_DATABASE_USER'),
    'password': os.environ.get('DEMO_DATABASE_PASSWORD'),
    'port': os.environ.get('DEMO_DATABASE_PORT'),
}

LINE_CHATBOT_API_KEY = os.environ.get('LINE_CHATBOT_API_KEY')
LINE_API = 'https://api.line.me/v2/bot/message/push'

tz = pytz.timezone('Asia/Bangkok')

@csrf_exempt
def list_user(request):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    conn.autocommit = False
    cursor.execute('''select * from "4urney".users''')
    rows = cursor.fetchall()
    formatted_data = []
    for row in rows:
        column_names = [desc[0] for desc in cursor.description]
        row_data = {column_names[i]: row[i] for i in range(len(column_names))}
        row_data['timestamp'] = str(row_data['timestamp'].astimezone(tz))
        formatted_data.append(row_data)
    cursor.close()
    conn.close()

    # users = User.objects.all()
    # data = serialize('json', users)
    return JsonResponse(formatted_data, safe=False)

@login_required
def list_user_test(request):
    user = User.objects.get(username=request.user)
    organization_member = OrganizationMember.objects.filter(user=user).first()
    organization = organization_member.organization
    customers = Customer.objects.filter(organization_id=organization)
    # customers = Customer.objects.all()
    customer_list = []
    for customer in customers:
        customer_data = {
            "id": customer.platform_id,
            "img": customer.img if customer.img else "",
            "name": customer.name if customer.name else "",
            "tag": customer.tag if customer.tag else "",
            "priority": customer.priority if customer.priority else "",
            "lastestMsg": customer.lastest_msg if customer.lastest_msg else "",
            "timestamp": customer.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S%z") if customer.timestamp else "",
            "isUrgent": customer.is_urgent if customer.is_urgent is not None else False,
            "provider": customer.provider if customer.provider else "",
            "agent": customer.agent if customer.agent else "",
            "messageType": customer.message_type if customer.message_type else "",
            "replyToken": customer.reply_token if customer.reply_token else None
        }
        customer_list.append(customer_data)

    # Return the response as JSON
    return JsonResponse(customer_list, safe=False)

def list_message(request, user_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    conn.autocommit = False
    cursor.execute(
        f'''select id, message, by, "timestamp" from "4urney".messages where id = '{user_id}' order by "timestamp" desc''')
    rows = cursor.fetchall()
    formatted_data = []
    for row in rows:
        column_names = [desc[0] for desc in cursor.description]
        column_names = ['id', 'msg', 'by', 'timestamp']
        row_data = {column_names[i]: row[i] for i in range(len(column_names))}
        row_data['timestamp'] = str(row_data['timestamp'].astimezone(tz))
        formatted_data.append(row_data)
    cursor.execute(f'''select "messageType" from "4urney".users where id='{user_id}' ''')
    result = cursor.fetchone()
    if result:
        data = dict(
            messageType=result[0],
            chatLogs=formatted_data,
        )
    else:
        data = dict(
            messageType='',
            chatLogs=formatted_data,
        )
    cursor.close()
    conn.close()

    return JsonResponse(data, safe=False)

def list_message_test(request, user_id):
    try:
        customer = Customer.objects.get(platform_id=user_id)
        message_type = customer.message_type if customer.message_type else "Unknown Message Type"
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=400)
    messages = Message.objects.filter(platform_id=customer).order_by('timestamp')
    chat_logs = []
    for message in messages:
        if message.timestamp:
            message_timestamp = message.timestamp.astimezone(tz)
            timestamp_str = message_timestamp.strftime("%Y-%m-%d %H:%M:%S%z")
        else:
            timestamp_str = ""
        chat_log = {
            "id": message.platform_id.platform_id if message.platform_id else "",  # Link to the customer platform_id
            "msg": message.message if message.message else "",
            "by": message.by if message.by else "unknown",
            "timestamp": timestamp_str
        }
        chat_logs.append(chat_log)
    response_data = {
        "messageType": message_type,
        "chatLogs": chat_logs
    }
    return JsonResponse(response_data, safe=False)

def admin_reply_post(request):
    data = request.data
    id = data['id']
    message = data['message']

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    conn.autocommit = False
    insert_query = '''
    INSERT INTO "4urney".messages (id, message, "by", "timestamp")
    VALUES (%s, %s, %s, %s)
    '''

    data_to_insert = (
        id,
        message,
        'admin',
        datetime.now()
    )

    cursor.execute(insert_query, data_to_insert)
    conn.commit()

    Authorization = f'Bearer {LINE_CHATBOT_API_KEY}'

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "to": f"{id}",
        "messages": [
            {
                "type": "text",
                "text": f"{message}"
            }
        ]
    }

    data = json.dumps(data)
    response = requests.post(LINE_API, headers=headers, data=data)

    cursor.execute(f'''select * from "4urney".messages where id = '{id}' order by "timestamp" desc''')
    rows = cursor.fetchall()
    formatted_data = []
    for row in rows:
        column_names = ['id','msg','by','timestamp']
        row_data = {column_names[i]: row[i] for i in range(len(column_names))}
        row_data['timestamp'] = str(row_data['timestamp'].astimezone(tz))
        formatted_data.append(row_data)
    cursor.close()
    conn.close()
    return JsonResponse(formatted_data, safe=False)

@csrf_exempt
def admin_reply_post_test(request):
    data = json.loads(request.body)
    id = data.get('id')
    message = data.get('message')

    username = request.user

    if not id or not message:
        return JsonResponse({"error": "Missing 'id' or 'message' in request"}, status=400)
    try:
        customer = Customer.objects.get(platform_id=id)
        message_type = customer.message_type if customer.message_type else "Unknown Message Type"
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found"}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=400)

    new_message = Message.objects.create(
        platform_id=customer,
        message=message,
        by='admin',
        user=user,
        timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
        organization_id=customer.organization_id,
    )

    organization_member = OrganizationMember.objects.filter(user=user).first()
    LINE_CHATBOT_API_KEY = LineIntegration.objects.filter(organization_id=organization_member.organization_id).first().line_chatbot_api_key
    Authorization = f'Bearer {LINE_CHATBOT_API_KEY}'

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data_to_send = {
        "to": id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post(LINE_API, headers=headers, data=json.dumps(data_to_send))

    messages = Message.objects.filter(platform_id=customer).order_by('-timestamp')

    tz = pytz.timezone('Asia/Bangkok')  # Ensure the timezone for formatting timestamps
    formatted_data = []
    for msg in messages:
        formatted_data.append({
            "id": msg.platform_id.platform_id if msg.platform_id else "",
            "msg": msg.message if msg.message else "",
            "by": msg.by if msg.by else "",
            "timestamp": msg.timestamp.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S%z"),
            "user": msg.user.username if msg.user else ""
        })

    # channel_layer = get_channel_layer()
    # group_name = f'organization_{organization_member.organization.id}'

    response_data = {
        "id": id,
        "messageType": message_type,
        "chatLogs": formatted_data
    }

    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {
    #         'type': 'send_json_to_client',
    #         'event': {
    #             'id': id,
    #             'type': 'message_update',
    #             'formatted_data': response_data
    #         }
    #     }
    # )

    return JsonResponse(response_data, safe=False)

def change_message_type(request):
    if request.method == 'POST':
        data = request.json()
        id = data['id']
        message_type = data['messageType']

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        conn.autocommit = False
        if message_type == 'Closed Messages':
            update_query_closed_to_opened = f'''
                UPDATE "4urney".users
                SET "messageType" = 'Opened Messages'
                WHERE "messageType" = 'Closed Messages' and id = '{id}'
                '''

            cursor.execute(update_query_closed_to_opened)
            conn.commit()

            cursor.execute('''select * from "4urney".users''')
            rows = cursor.fetchall()
            formatted_data = []
            for row in rows:
                column_names = [desc[0] for desc in cursor.description]
                row_data = {column_names[i]: row[i] for i in range(len(column_names))}
                row_data['timestamp'] = str(row_data['timestamp'].astimezone(tz))
                formatted_data.append(row_data)
            cursor.close()
            conn.close()

            return JsonResponse({'messageType': 'Opened Messages', 'listUser': formatted_data})
        elif message_type == 'Opened Messages':
            update_query_opened_to_closed = f'''
                UPDATE "4urney".users
                SET "messageType" = 'Closed Messages'
                WHERE "messageType" = 'Opened Messages' and id = '{id}'
                '''

            cursor.execute(update_query_opened_to_closed)
            conn.commit()

            cursor.execute('''select * from "4urney".users''')
            rows = cursor.fetchall()
            formatted_data = []
            for row in rows:
                column_names = [desc[0] for desc in cursor.description]
                row_data = {column_names[i]: row[i] for i in range(len(column_names))}
                formatted_data.append(row_data)
            cursor.close()
            conn.close()

            return JsonResponse({'messageType': 'Closed Messages', 'listUser': formatted_data})

def change_message_type_test(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        message_type = data.get('messageType')

        if not id or not message_type:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        try:
            customer = Customer.objects.get(platform_id=id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        if message_type == 'Closed Messages':
            customer.message_type = 'Opened Messages'
            customer.save()

            customers = Customer.objects.filter(message_type='Opened Messages')
            customers_data = [{
                'platform_id': customer.platform_id,
                'messageType': customer.message_type,
                'timestamp': customer.timestamp.astimezone(tz).strftime(
                    "%Y-%m-%d %H:%M:%S%z"),
                'name': customer.name,  # Include any other fields you need
                'tag': customer.tag,
                'priority': customer.priority
            } for customer in customers]

            return JsonResponse({'messageType': 'Opened Messages', 'listCustomer': customers_data})
        elif message_type == 'Opened Messages':
            customer.message_type = 'Closed Messages'
            customer.save()

            customers = Customer.objects.filter(message_type='Closed Messages')
            customers_data = [{
                'platform_id': customer.platform_id,
                'messageType': customer.message_type,
                'timestamp': customer.timestamp.astimezone(tz).strftime(
                    "%Y-%m-%d %H:%M:%S%z"),
                'name': customer.name,  # Include any other fields you need
                'tag': customer.tag,
                'priority': customer.priority
            } for customer in customers]

            return JsonResponse({'messageType': 'Closed Messages', 'listCustomer': customers_data})
        else:
            return JsonResponse({'error': 'Invalid messageType'}, status=400)

def list_dashboard(request, id):
    print(id)
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    conn.autocommit = False
    cursor.execute(f'''SELECT * FROM "4urney".dashboard WHERE id = '{id}' ''')
    result = cursor.fetchone()
    cursor.execute(f'''select summarize from "4urney".chat_summarize where user_id='{id}' ''')
    summarize = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        (id, name, gender, phonenumber, citizenid, birthday, email,
         satisfaction, dissatisfaction, totalsession, totalmessage, urgent,
         priority, intentsummary) = result

        data = {
            "id": id,
            "userInformation": {
                "name": name,
                "gender": gender,
                "phoneNumber": phonenumber,
                "citizenId": citizenid,
                "birthday": birthday,
                "email": email,
            },
            "dashboard": {
                "satisfaction": satisfaction,
                "dissatisfaction": dissatisfaction,
                "totalSession": totalsession,
                "totalMessage": totalmessage,
                "urgent": urgent,
                "priority": priority,
                "intentSummary": summarize[0].split('\n') if summarize else [],
            }
        }

        return JsonResponse(data, safe=False)

    else:
        data = {
            "dashboard": {
                "dissatisfaction": 0,
                "intentSummary": [

                ],
                "priority": None,
                "satisfaction": 0,
                "totalMessage": 0,
                "totalSession": 0,
                "urgent": 0
            },
            "id": "-1",
            "userInformation": {
                "birthday": "untitled",
                "citizenId": "untitled",
                "email": "untitled",
                "gender": "untitled",
                "name": "untitled",
                "phoneNumber": "untitled"
            }
        }
        return JsonResponse(data, safe=False)

def list_dashboard_test(request, id):
    try:
        dashboard = Dashboard.objects.get(platform_id=id)
    except Dashboard.DoesNotExist:
        customer = Customer.objects.get(platform_id=id)
        dashboard = Dashboard.objects.create(
            platform_id=customer,
            name="untitled",
            gender="untitled",
            phonenumber="untitled",
            citizenid="untitled",
            birthday="untitled",
            email="untitled",
            satisfaction=None,
            dissatisfaction=None,
            totalsession=None,
            totalmessage=None,
            urgent=None,
            priority=None,
            intentsummary=None,
        )

    satisfaction = ChatUserSatisfaction.objects.filter(platform_id=id).first()
    urgent = ChatUserUrgent.objects.filter(platform_id=id).first()
    summarize = ChatSummarize.objects.filter(platform_id=id).first()

    messages_by_bot = Message.objects.filter(by='bot', platform_id=id) \
        .values('platform_id') \
        .annotate(message_count=Count('id')) \
        .order_by('platform_id')
    for message in messages_by_bot:
        count_message = message['message_count']
        print(f"Platform ID: {message['platform_id']}, Message Count: {message['message_count']}")

    response_data = {
        "dissatisfaction": dashboard.dissatisfaction if dashboard.dissatisfaction is not None else 0,
        "intentSummary": summarize.summarize.split('\n') if summarize.summarize else [],
        "priority": dashboard.priority if dashboard.priority else None,
        "satisfaction": satisfaction.satisfaction if satisfaction.satisfaction is not None else 0,
        "totalMessage": dashboard.totalmessage if dashboard.totalmessage is not None else 0,
        "totalSession": dashboard.totalsession if dashboard.totalsession is not None else 0,
        "urgent": urgent.urgent if urgent.urgent is not None else 0,
        "id": dashboard.id,
        "userInformation": {
            "birthday": dashboard.birthday if dashboard.birthday else "untitled",
            "citizenId": dashboard.citizenid if dashboard.citizenid else "untitled",
            "email": dashboard.email if dashboard.email else "untitled",
            "gender": dashboard.gender if dashboard.gender else "untitled",
            "name": dashboard.name if dashboard.name else "untitled",
            "phoneNumber": dashboard.phonenumber if dashboard.phonenumber else "untitled"
        },
        "countBotMessage": count_message,
    }

    return JsonResponse(response_data)

def edit_customer_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        gender = data.get('gender')
        birthday = data.get('birthday')
        phonenumber = data.get('phoneNumber')
        citizenid = data.get('citizenId')

        dashboard = Dashboard.objects.get(id=id)
        dashboard.name = name
        dashboard.email = email
        dashboard.gender = gender
        dashboard.birthday = birthday
        dashboard.phonenumber = phonenumber
        dashboard.citizenid = citizenid
        dashboard.save()

        dashboard_data = Dashboard.objects.filter(id=id).first()

        satisfaction = ChatUserSatisfaction.objects.filter(platform_id=dashboard_data.platform_id.platform_id).first()
        urgent = ChatUserUrgent.objects.filter(platform_id=dashboard_data.platform_id.platform_id).first()
        summarize = ChatSummarize.objects.filter(platform_id=dashboard_data.platform_id.platform_id).first()

        response_data = {
            "dissatisfaction": dashboard.dissatisfaction if dashboard.dissatisfaction is not None else 0,
            "intentSummary": summarize.summarize.split('\n') if summarize else [],
            "priority": dashboard.priority if dashboard.priority else None,
            "satisfaction": satisfaction.satisfaction if satisfaction is not None else 0,
            "totalMessage": dashboard.totalmessage if dashboard.totalmessage is not None else 0,
            "totalSession": dashboard.totalsession if dashboard.totalsession is not None else 0,
            "urgent": urgent.urgent if urgent is not None else 0,
            "id": dashboard.id,
            "userInformation": {
                "birthday": dashboard.birthday if dashboard.birthday else "untitled",
                "citizenId": dashboard.citizenid if dashboard.citizenid else "untitled",
                "email": dashboard.email if dashboard.email else "untitled",
                "gender": dashboard.gender if dashboard.gender else "untitled",
                "name": dashboard.name if dashboard.name else "untitled",
                "phoneNumber": dashboard.phonenumber if dashboard.phonenumber else "untitled"
            }
        }

        return JsonResponse(response_data)


def get_user_detail(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_dict = model_to_dict(user)
        if request.user.is_superuser:
            return JsonResponse(user_dict, status=status.HTTP_200_OK)
        organization_member = OrganizationMember.objects.filter(user=user).first()
        if organization_member:
            organization_id = organization_member.organization.id
            print("Organization ID:", organization_id)
            return JsonResponse(user_dict, status=status.HTTP_200_OK)
        else:
            print("User is not a member of any organization.")
            return JsonResponse({"detail": "User is not a member of any organization."}, status=status.HTTP_403_FORBIDDEN)
    else:
        return JsonResponse({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)


class FileUploadView(APIView):
    queryset = UploadedFile.objects.all()

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.user)
        organization_member = OrganizationMember.objects.filter(user=request.user).first()
        organization_name = organization_member.organization.name
        organization = organization_member.organization
        user = User.objects.get(username=request.user)
        email = user.email
        serializer = FileUploadSerializer(data=request.data)


        if serializer.is_valid():
            uploaded_file = serializer.save(organization_member=organization_member, user=email, description=request.data['description'], organization_id=organization)
            print(f'file_path {uploaded_file.file}')
            data = boto3.client('s3').generate_presigned_post(settings.AWS_STORAGE_BUCKET_NAME, uploaded_file.file.name)

            print(f"Uploaded file name: {uploaded_file.file.name}")
            print(f"File stored at: {uploaded_file.file.url}")

            # return JsonResponse({"message": "File uploaded and processed successfully!"}, status=200)
            return JsonResponse(data, status=200)

        return JsonResponse({"message": "File upload failed", "errors": serializer.errors}, status=400)


def create_bot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_name = data.get('bot_name')
        routing = data.get('routing')
        prompt = data.get('prompt')
        industry = data.get('industry')
        retrieve_image = data.get('retrieve_image')
        knowledge_base = data.get('knowledge_base')
        is_active = data.get('isActive')
        line_integration_uuid = data.get('line_integration_uuid')

        user = request.user
        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization

        routing_chain = RoutingChain.objects.create(
            bot_name=bot_name,
            routing=routing,
            prompt=prompt,
            industry=industry,
            retrieve_image=retrieve_image,
            knowledge_base=knowledge_base,
            is_active=is_active,
            created_at=datetime.now(),
            organization_id=organization,
        )

        line_integration = LineIntegration.objects.filter(uuid=line_integration_uuid).first()
        if not line_integration:
            LineConnectionNew.objects.create(
                bot_id=routing_chain,
                uuid=None,
            )
            return JsonResponse({"message": "Create bot successfully without line integration."}, status=200)

        LineConnectionNew.objects.create(
            bot_id=routing_chain,
            uuid=line_integration,
        )

        return JsonResponse({"message": "Create bot successfully with line integration."}, status=200)

def list_line_integration(request):
    line_integrations = LineIntegration.objects.all()
    # uuids = [integration.uuid for integration in line_integrations]
    line_integration_data = [
        {
            'uuid': integration.uuid,
            'user_id': integration.user_id,
            'username': integration.username,
        }
        for integration in line_integrations
    ]
    return JsonResponse(line_integration_data, safe=False)

def list_industry_choices(request):
    industry_choices = RoutingChain._meta.get_field('industry').choices
    industry_values = [choice[0] for choice in industry_choices]

    return JsonResponse(industry_values, safe=False)


def list_upload_file(request):
    file_details = list(UploadedFile.objects.values('id', 'file', 'uploaded_at', 'collection_name', 'embedded_date', 'status', 'user', 'description'))
    for file in file_details:
        file['file_url'] = f'https://{os.environ['AWS_STORAGE_BUCKET_NAME']}.s3.amazonaws.com/{file['file']}'
        file['file_name'] = file['file'].split('/')[-1]

    return JsonResponse(file_details, safe=False)

def remove_upload_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')

        data = UploadedFile.objects.get(id=id)
        data.delete()

        file_details = list(UploadedFile.objects.values('id', 'file', 'uploaded_at', 'collection_name', 'embedded_date', 'status', 'user', 'description'))
        for file in file_details:
            file['file_url'] = f'https://{os.environ['AWS_STORAGE_BUCKET_NAME']}.s3.amazonaws.com/{file['file']}'
            file['file_name'] = file['file'].split('/')[-1]

        return JsonResponse(file_details, safe=False)

def edit_upload_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        description = data.get('description')

        data = UploadedFile.objects.get(id=id)
        data.description = description
        data.save()

        file_details = list(UploadedFile.objects.values('id', 'file', 'uploaded_at', 'collection_name', 'embedded_date', 'status', 'user', 'description'))
        for file in file_details:
            file['file_url'] = f'https://{os.environ['AWS_STORAGE_BUCKET_NAME']}.s3.amazonaws.com/{file['file']}'
            file['file_name'] = file['file'].split('/')[-1]

        return JsonResponse(file_details, safe=False)


def summarize_dashboard(request, user_id):
    # user_id = 'U32afe3db274f527b57262faf86bb1359'
    
    tracer = LangChainTracer(project_name="Dashboard Chat Insight")

    llms = ChatOpenAI(
        temperature=0.7,  # Controls randomness of responses
        max_tokens=1024,  # Maximum token count in responses
        model="gpt-4o"  # Model version
    )
    customer = Customer.objects.get(platform_id=user_id)
    # Task 1: Summarize conversations
    df_msgs = pd.DataFrame(list(Message.objects.filter(platform_id=customer).values('platform_id', 'message', 'by', 'user', 'timestamp', 'organization_id')))

    df_sums_query = ChatSummarize.objects.filter(platform_id=user_id)

    if df_sums_query.exists():
        df_sums = pd.DataFrame(
            list(df_sums_query.values('platform_id', 'summarize', 'lastest_msg_date', 'generated_date')))
    else:
        df_sums = pd.DataFrame(columns=['platform_id', 'summarize', 'lastest_msg_date', 'generated_date'])

    focus_user_ids, grouped = preprocess_data(df_msgs.copy(), df_sums, summary_col='lastest_msg_date')

    data = process_task(focus_user_ids, grouped, llms, summarize_conversation, "chat_summarize", "summarize", tracer)
    ChatSummarize.objects.update_or_create(
        platform_id=user_id,
        defaults={
            "summarize": data['result'],
            "lastest_msg_date": data['lastest_msg_date'],
            "generated_date": timezone.now(),
        }
    )

    # Task 2: Score customer satisfaction
    df_sats_query = ChatUserSatisfaction.objects.filter(platform_id=user_id)

    if df_sats_query.exists():
        df_sats = pd.DataFrame(
            list(df_sats_query.values('platform_id', 'satisfaction', 'lastest_msg_date', 'generated_date')))
    else:
        df_sats = pd.DataFrame(columns=['platform_id', 'satisfaction', 'lastest_msg_date', 'generated_date'])

    focus_user_ids, grouped = preprocess_data(df_msgs.copy(), df_sats, summary_col='lastest_msg_date')

    data = process_task(focus_user_ids, grouped, llms, score_satisfaction, "chat_user_satisfaction", "satisfaction", tracer)

    ChatUserSatisfaction.objects.update_or_create(
        platform_id=user_id,
        defaults={
            "satisfaction": data['result'],
            "lastest_msg_date": data['lastest_msg_date'],
            "generated_date": timezone.now(),
        }
    )

    # Task 3: Identify urgent user interactions
    df_urg_query = ChatUserUrgent.objects.filter(platform_id=user_id)

    if df_urg_query.exists():
        df_urg = pd.DataFrame(
            list(df_urg_query.values('platform_id', 'urgent', 'lastest_msg_date', 'generated_date')))
    else:
        df_urg = pd.DataFrame(columns=['platform_id', 'urgent', 'lastest_msg_date', 'generated_date'])

    focus_user_ids, grouped = preprocess_data(df_msgs.copy(), df_urg, summary_col='lastest_msg_date')

    data = process_task(focus_user_ids, grouped, llms, score_urgency, "chat_user_urgent", "urgent", tracer)

    ChatUserUrgent.objects.update_or_create(
        platform_id=user_id,
        defaults={
            "urgent": data['result'],
            "lastest_msg_date": data['lastest_msg_date'],
            "generated_date": timezone.now(),
        }
    )

    return JsonResponse({"message": "Done"}, status=200)

async def process_file_async(file_path, file_extension, collection_name, uploaded_file):
    if file_extension == 'xlsx':
        print('Processing Excel file...')
        whole_df = await asyncio.to_thread(process_excel, file_path=file_path, client=client)
        await asyncio.to_thread(data_ingestion_df, data=whole_df, collection_name=collection_name)
    elif file_extension == 'csv':
        print('Processing CSV file...')
        ready_data = await asyncio.to_thread(process_csv, file_path=file_path, client=client)
        await asyncio.to_thread(data_ingestion_df, data=ready_data, collection_name=collection_name)
    elif file_extension == 'pdf':
        print('Processing PDF file...')
        docs = await asyncio.to_thread(process_pdf, file_path)
        await asyncio.to_thread(read_push_document, docs=docs, collection_name=collection_name, client=client)
    elif file_extension in ['jpeg', 'jpg']:
        pass
    else:
        print('Unknown file type.')

    # Update the UploadedFile model
    uploaded_file.collection_name = collection_name
    uploaded_file.embedded_date = datetime.now()
    await asyncio.to_thread(uploaded_file.save)

# class EmbeddedDataView(View):
#     async def get(self, request, *args, **kwargs):
#         load_dotenv()
#
#         bucket_name = os.environ['AWS_STORAGE_BUCKET_NAME']
#         save_dir = './downloads/'
#
#         # Fetch file from S3 (this is an I/O-bound operation and can be async)
#         s3_url = "https://4urney-dev-data-model.s3.amazonaws.com/Demo/EC_EI_008_S2.xlsx"
#         bucket_name, object_name = extract_bucket_and_object(s3_url)
#         await asyncio.to_thread(save_file_in_original_format, bucket_name, object_name, save_dir)
#
#         org_name, file_name, file_path, collection_name = get_file_details(object_name, save_dir)
#
#         # Connect to Milvus asynchronously (Database connection can be offloaded to a thread)
#         await asyncio.to_thread(connections.connect, "default", host=os.environ['MILVUS_HOST'], port=os.environ['MILVUS_PORT'])
#
#         # Get the UploadedFile instance to update
#         uploaded_file = await asyncio.to_thread(UploadedFile.objects.get, file__exact=object_name)
#
#         file_extension = object_name.split('.')[-1]
#
#         # Process the file asynchronously (offload long-running tasks to separate threads)
#         await process_file_async(file_path, file_extension, collection_name, uploaded_file)
#
#         # Cleanup after processing (run in a separate thread)
#         await asyncio.to_thread(delete_save_dir, save_dir)
#
#         return JsonResponse({"message": "Embedded file successfully!"}, status=200)


class TaskStatusView(View):
    def get(self, request, *args, **kwargs):
        # file_name = kwargs.get('file_name')

        file_name = 'Demo/EC_EI_008_S2.xlsx'
        uploaded_file = get_object_or_404(UploadedFile, file__exact=file_name)

        if uploaded_file.embedded_date:
            return JsonResponse({"status": "Completed", "embedded_date": uploaded_file.embedded_date})
        else:
            return JsonResponse({"status": "Pending"})

def process_file_in_background(file_path, file_extension, collection_name, uploaded_file_id, client, llms):
    uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)

    if file_extension == 'xlsx':
        print('Processing Excel file...')
        whole_df = process_excel(file_path, client)
        data_ingestion_df(data=whole_df, collection_name=collection_name)
    elif file_extension == 'csv':
        print('Processing CSV file...')
        ready_data = process_csv(file_path, client)
        data_ingestion_df(data=ready_data, collection_name=collection_name)
    elif file_extension == 'pdf':
        print('Processing PDF file...')
        docs = process_pdf(file_path)
        read_push_document(docs=docs, collection_name=collection_name, client=client)
    elif file_extension in ['jpeg', 'jpg']:
        print('Processing IMAGE file...')
        docs = process_image(file_path, llms)
        read_push_document(docs=docs, collection_name=collection_name, client=client)
    else:
        print('Unknown file type.')

    uploaded_file.collection_name = collection_name
    uploaded_file.embedded_date = datetime.now()
    uploaded_file.status = 'Completed'
    uploaded_file.save()
    save_dir = './downloads/'
    delete_save_dir(save_dir)
    print('Done')

class EmbeddedDataView(View):
    def get(self, request, *args, **kwargs):
        load_dotenv()
        
        client = OpenAI()   
        llms = ChatOpenAI(
                            temperature=0.7,  # Controls randomness of responses
                            max_tokens=1024,  # Maximum token count in responses
                            model="gpt-4o"  # Model version
                        )

        save_dir = './downloads/'

        s3_url = "https://4urney-dev-data-model.s3.amazonaws.com/Demo/EC_EI_008_S2.xlsx"
        bucket_name, object_name = extract_bucket_and_object(s3_url)
        save_file_in_original_format(bucket_name, object_name, save_dir)

        org_name, file_name, file_path, collection_name = get_file_details(object_name, save_dir)

        connections.connect("default", host=os.environ['MILVUS_HOST'], port=os.environ['MILVUS_PORT'])

        uploaded_file = UploadedFile.objects.get(file__exact=object_name)
        uploaded_file.status = 'Processing'
        uploaded_file.save()

        file_extension = object_name.split('.')[-1]

        threading.Thread(target=process_file_in_background, args=(file_path, file_extension, collection_name, uploaded_file.id, client, llms)).start()

        return JsonResponse({"message": "Embedding task has been started."}, status=200)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        s3_url = data.get('file_url', None)

        print(s3_url)

        if not s3_url:
            return JsonResponse({"error": "s3_url parameter is required."}, status=400)

        load_dotenv()
        
        client = OpenAI()

        llms = ChatOpenAI(
                            temperature=0.7,  # Controls randomness of responses
                            max_tokens=1024,  # Maximum token count in responses
                            model="gpt-4o"  # Model version
                        )
        
        save_dir = f'./downloads/{short_uuid4()}'

        bucket_name, object_name = extract_bucket_and_object(s3_url)
        save_file_in_original_format(bucket_name, object_name, save_dir)

        org_name, file_name, file_path, collection_name = get_file_details(object_name, save_dir)

        connections.connect("default", host=os.environ['MILVUS_HOST'], port=os.environ['MILVUS_PORT'])

        uploaded_file = UploadedFile.objects.get(file__exact=object_name)
        uploaded_file.status = 'Processing'
        uploaded_file.save()

        file_extension = object_name.split('.')[-1]

        threading.Thread(target=process_file_in_background, args=(file_path, file_extension, collection_name, uploaded_file.id, client, llms)).start()

        return JsonResponse({"message": "Embedding task has been started."}, status=200)

def list_knowledge_base(request):
    connections.connect("default", host=os.environ['MILVUS_HOST'], port=os.environ['MILVUS_PORT'])
    all_collection_names = utility.list_collections()

    username = request.user
    user = User.objects.get(username=username)

    organization_member = OrganizationMember.objects.filter(user=user).first()
    org_name = organization_member.organization.name

    focus_collection_names = [name for name in all_collection_names if name.find(org_name) > -1]

    return JsonResponse(focus_collection_names, safe=False)

def list_bot(request):
    username = request.user
    user = User.objects.get(username=username)

    organization_member = OrganizationMember.objects.filter(user=user).first()
    organization = organization_member.organization

    queryset = RoutingChain.objects.filter(organization_id=organization).values(
        'id',
        'bot_name',
        'industry',
        'routing',
        'is_active'
    )

    # Map the queryset to the desired format
    formatted_data = [
        {
            'id': item['id'],
            'img': '',
            'name': item['bot_name'],
            'industry': item['industry'],
            'mastery': item['routing'],
            'isActive': item['is_active'],
        }
        for item in queryset
    ]

    return JsonResponse(formatted_data, safe=False)

def create_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_id = data.get('id')
        session_name = data.get('sessionName')

        routing_chain = RoutingChain.objects.get(id=bot_id)
        user = request.user
        user = User.objects.get(username=user)

        new_session = InternalChatSession(session_name=session_name, bot_id=routing_chain, user=user, timestamp=datetime.now())
        new_session.save()

        queryset = InternalChatSession.objects.filter(bot_id=routing_chain, user=user).values(
            'id',
            'session_name',
            'timestamp',
        )

        formatted_data = [
            {
                'id': item['id'],
                'name': item['session_name'],
                'lastConversationTime': item['timestamp'].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S%z") if item['timestamp'] else None,
            }
            for item in queryset
        ]

        return JsonResponse(formatted_data, safe=False)

def list_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_id = data.get('id')

        routing_chain = RoutingChain.objects.get(id=bot_id)
        user = request.user
        user = User.objects.get(username=user)

        queryset = InternalChatSession.objects.filter(bot_id=routing_chain, user=user).values(
            'id',
            'session_name',
            'timestamp'
        )

        formatted_data = [
            {
                'id': item['id'],
                'name': item['session_name'],
                'lastConversationTime': item['timestamp'].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S%z") if item['timestamp'] else None,
            }
            for item in queryset
        ]

        return JsonResponse(formatted_data, safe=False)

def rename_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        bot_id = data.get('id')  # bot_id (RoutingChain ID)
        session_id = data.get('sessionId')  # The session to rename
        new_session_name = data.get('newSessionName')  # The new name for the session

        routing_chain = RoutingChain.objects.get(id=bot_id)
        user = request.user
        user = User.objects.get(username=user)

        session = InternalChatSession.objects.get(id=session_id, bot_id=routing_chain)
        session.session_name = new_session_name
        session.save()

        queryset = InternalChatSession.objects.filter(bot_id=routing_chain, user=user).values(
            'id',
            'session_name',
            'timestamp',
        )

        formatted_data = [
            {
                'id': item['id'],
                'name': item['session_name'],
                'lastConversationTime': item['timestamp'].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S%z") if item['timestamp'] else None,
            }
            for item in queryset
        ]

        return JsonResponse(formatted_data, safe=False)


def remove_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        bot_id = data.get('id')
        session_id = data.get('sessionId')

        routing_chain = RoutingChain.objects.get(id=bot_id)
        user = request.user
        user = User.objects.get(username=user)
        session = InternalChatSession.objects.get(id=session_id, bot_id=routing_chain)
        session.delete()

        queryset = InternalChatSession.objects.filter(bot_id=routing_chain, user=user).values(
            'id',
            'session_name',
            'timestamp',
        )

        formatted_data = [
            {
                'id': item['id'],
                'name': item['session_name'],
                'lastConversationTime': item['timestamp'].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S%z") if item['timestamp'] else None,
            }
            for item in queryset
        ]

        return JsonResponse(formatted_data, safe=False)


def get_internal_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        bot_id = data.get('id')  # bot_id (RoutingChain ID)
        session_id = data.get('sessionId')  # The session ID
        user = request.user
        user = User.objects.get(username=user)
        routing_chain = RoutingChain.objects.get(id=bot_id)
        session = InternalChatSession.objects.get(id=session_id, bot_id=routing_chain)

        messages = InternalChatMessage.objects.filter(session_id=session, bot_id=routing_chain, user=user)

        formatted_messages = [
            {
                'id': message.id,
                'msg': message.message,
                'by': message.by,
                'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S%z") if message.timestamp else None
            }
            for message in messages
        ]

        return JsonResponse(formatted_messages, safe=False)


@csrf_exempt
def internal_chatbot(request):
    """
    Processes POST requests to handle chatbot interactions.

    Extracts `bot_id`, `user_id`, and `message` from the request, retrieves chat history and bot configurations,
    checks the user's status, and routes the message to generate a bot response. If the user is in "Opened Messages"
    status, no response is generated. Utilizes asynchronous database queries and external API calls for routing
    and knowledge base retrieval.

    Args:
        request (HttpRequest): The incoming HTTP request object. It should contain
                               the `bot_id`, `user_id`, and `message` in its JSON body.

    Returns:
        HttpResponse or JsonResponse:
            - If the user's status is not "Opened Messages," it returns the bot's response.
            - If the user's status is "Opened Messages," it logs a message and does not
              generate a bot response.
    """
    EMBEDDING_MODEL_API = os.environ.get('EMBEDDING_MODEL_API')
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_id = data.get('id')
        session_id = data.get('sessionId')
        message = data.get('msg')
        user = request.user
        print(user)

        routing_chain = RoutingChain.objects.get(id=bot_id)
        session = InternalChatSession.objects.get(id=session_id, bot_id=routing_chain)
        user = User.objects.get(username=user)
        # latest_messages = await sync_to_async(list)(InternalChatMessage.objects.filter(session_id=session, bot_id=routing_chain).all().order_by('-timestamp')[:10])
        latest_messages = InternalChatMessage.objects.filter(
            session_id=session, bot_id=routing_chain, user=user,
        ).order_by('-timestamp')[:10]
        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization

        new_message = InternalChatMessage.objects.create(
            message=message,
            by='user',
            user=user,
            bot_id=routing_chain,
            session_id=session,
            timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
            organization_id=organization,
        )

        # message_counts = InternalChatMessage.objects.filter(by='bot', organization_id=organization) \
        #     .values('organization_id') \
        #     .annotate(message_count=Count('id'))
        #
        # for result in message_counts:
        #     count_message = result['message_count']
        #
        # if count_message >= 10:
        #     new_bot_message = InternalChatMessage.objects.create(
        #         message='ขออภัยค่ะ โควต้าบอทตอบหมด',
        #         by='system',
        #         user=user,
        #         bot_id=routing_chain,
        #         session_id=session,
        #         timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
        #         organization_id=organization,
        #     )
        #
        #     messages = InternalChatMessage.objects.filter(
        #         session_id=session, bot_id=routing_chain, user=user,
        #     ).order_by('timestamp')
        #     chat_logs = []
        #     for message in messages:
        #         if message.timestamp:
        #             message_timestamp = message.timestamp.astimezone(tz)
        #             timestamp_str = message_timestamp.strftime("%Y-%m-%d %H:%M:%S%z")
        #         else:
        #             timestamp_str = ""
        #         chat_log = {
        #             "id": message.id,
        #             "msg": message.message if message.message else "",
        #             "by": message.by if message.by else "unknown",
        #             "timestamp": timestamp_str
        #         }
        #         chat_logs.append(chat_log)
        #
        #     return JsonResponse(chat_logs, safe=False)


        print('New Message', new_message)
        chat_history = ""
        for history in latest_messages[::-1]:
            chat_history += f"{history.by}: {history.message}" + '\n'

        # routing_configs = await sync_to_async(lambda: list(RoutingChain.objects.filter(id=bot_id).values()))()
        routing_configs = RoutingChain.objects.filter(id=bot_id).values()
        df_routing_config = pd.DataFrame(routing_configs)
        print(df_routing_config)

        model_response = requests.post(EMBEDDING_MODEL_API, json={"msg": message, "milvus_collection": list(
            df_routing_config['knowledge_base']), "candidate_labels": list(df_routing_config['routing'])})

        print('Model response : ', model_response)

        retrieval_text = model_response.json()['retrieval_text']
        routing = model_response.json()['routing']

        responses_message = call_bot(chat_history=chat_history, routing=routing, message=message,
                                     retrieval_text=retrieval_text, df_routing_config=df_routing_config)
        responses_message = responses_message.content

        new_bot_message = InternalChatMessage.objects.create(
            message=responses_message,
            by='bot',
            user=user,
            bot_id=routing_chain,
            session_id=session,
            timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
            organization_id=organization,
        )

        messages = InternalChatMessage.objects.filter(
            session_id=session, bot_id=routing_chain, user=user,
        ).order_by('timestamp')
        chat_logs = []
        for message in messages:
            if message.timestamp:
                message_timestamp = message.timestamp.astimezone(tz)
                timestamp_str = message_timestamp.strftime("%Y-%m-%d %H:%M:%S%z")
            else:
                timestamp_str = ""
            chat_log = {
                "id": message.id,
                "msg": message.message if message.message else "",
                "by": message.by if message.by else "unknown",
                "timestamp": timestamp_str
            }
            chat_logs.append(chat_log)

        return JsonResponse(chat_logs, safe=False)
    elif request.method == 'GET':
        bot_id = 7
        session_id = 1
        message = 'testja'
        user = request.user
        print(user)

        routing_chain = RoutingChain.objects.get(id=bot_id)
        session = InternalChatSession.objects.get(id=session_id, bot_id=routing_chain)
        user = User.objects.get(username=user)
        # latest_messages = await sync_to_async(list)(InternalChatMessage.objects.filter(session_id=session, bot_id=routing_chain).all().order_by('-timestamp')[:10])
        latest_messages = InternalChatMessage.objects.filter(
            session_id=session, bot_id=routing_chain, user=user,
        ).order_by('-timestamp')[:10]
        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization

        new_message = InternalChatMessage.objects.create(
            message=message,
            by='user',
            user=user,
            bot_id=routing_chain,
            session_id=session,
            timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
            organization_id=organization,
        )

        print('New Message', new_message)
        chat_history = ""
        for history in latest_messages:
            chat_history += f"{history.by}: {history.message}" + '\n'

        # routing_configs = await sync_to_async(lambda: list(RoutingChain.objects.filter(id=bot_id).values()))()
        routing_configs = RoutingChain.objects.filter(id=bot_id).values()
        df_routing_config = pd.DataFrame(routing_configs)
        print(df_routing_config)

        model_response = requests.post(EMBEDDING_MODEL_API, json={"msg": message, "milvus_collection": list(
            df_routing_config['knowledge_base']), "candidate_labels": list(df_routing_config['routing'])})

        print('Model response : ',model_response)

        retrieval_text = model_response.json()['retrieval_text']
        routing = model_response.json()['routing']

        responses_message = call_bot(chat_history=chat_history, routing=routing, message=message,
                                     retrieval_text=retrieval_text, df_routing_config=df_routing_config)
        responses_message = responses_message.content


        new_bot_message = InternalChatMessage.objects.create(
            message=responses_message,
            by='bot',
            user=user,
            bot_id=routing_chain,
            session_id=session,
            timestamp=datetime.now(pytz.timezone('Asia/Bangkok')),
            organization_id=organization,
        )

        messages = InternalChatMessage.objects.filter(
            session_id=session, bot_id=routing_chain, user=user,
        ).order_by('timestamp')
        chat_logs = []
        for message in messages:
            if message.timestamp:
                message_timestamp = message.timestamp.astimezone(tz)
                timestamp_str = message_timestamp.strftime("%Y-%m-%d %H:%M:%S%z")
            else:
                timestamp_str = ""
            chat_log = {
                "id": message.id,
                "msg": message.message if message.message else "",
                "by": message.by if message.by else "unknown",
                "timestamp": timestamp_str
            }
            chat_logs.append(chat_log)

        return JsonResponse(chat_logs, safe=False)


def get_chatbot_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_id = int(data.get('id'))

        item = RoutingChain.objects.filter(id=bot_id).values(
            'id',
            'bot_name',
            'routing',
            'prompt',
            'industry',
            'retrieve_image',
            'routing',
            'knowledge_base',
            'is_active',
        ).first()

        routing_chain = RoutingChain.objects.get(id=bot_id)
        try:
            line_connection = LineConnectionNew.objects.filter(bot_id=routing_chain).values('uuid').first()
            print(line_connection)

            formatted_data = {
                'id': item['id'],
                'img': '',
                'bot_name': item['bot_name'],
                'routing': item['routing'],
                'prompt': item['prompt'],
                'industry': item['industry'],
                'retrieve_image': item['retrieve_image'],
                'knowledge_base': item['knowledge_base'],
                'isActive': item['is_active'],
                'line_integration_uuid': line_connection['uuid'] if line_connection else None,
            }
        except:
            formatted_data = {
                'id': item['id'],
                'img': '',
                'bot_name': item['bot_name'],
                'routing': item['routing'],
                'prompt': item['prompt'],
                'industry': item['industry'],
                'retrieve_image': item['retrieve_image'],
                'knowledge_base': item['knowledge_base'],
                'isActive': item['is_active'],
                'line_integration_uuid': None,
            }

        return JsonResponse(formatted_data, status=200)

def get_chatbot_data_new(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_id = int(data.get('id'))

        item = RoutingChain.objects.filter(id=bot_id).values(
            'id',
            'bot_name',
            'routing',
            'prompt',
            'industry',
            'retrieve_image',
            'routing',
            'knowledge_base',
            'is_active',
        ).first()

        routing_chain = RoutingChain.objects.get(id=bot_id)
        try:
            line_connection = LineConnectionNew.objects.filter(bot_id=routing_chain).values('uuid').first()
            print(line_connection)

            formatted_data = {
                'id': item['id'],
                'img': '',
                'bot_name': item['bot_name'],
                'routing': item['routing'],
                'prompt': item['prompt'],
                'industry': item['industry'],
                'retrieve_image': item['retrieve_image'],
                'knowledge_base': item['knowledge_base'],
                'isActive': item['is_active'],
                'line_integration_uuid': line_connection['uuid'] if line_connection else None,
            }
        except:
            formatted_data = {
                'id': item['id'],
                'img': '',
                'bot_name': item['bot_name'],
                'routing': item['routing'],
                'prompt': item['prompt'],
                'industry': item['industry'],
                'retrieve_image': item['retrieve_image'],
                'knowledge_base': item['knowledge_base'],
                'isActive': item['is_active'],
                'line_integration_uuid': None,
            }

        return JsonResponse(formatted_data, status=200)
    elif request.method == 'GET':
        bot_id = 7

        item = RoutingChain.objects.filter(id=bot_id).values(
            'id',
            'bot_name',
            'routing',
            'prompt',
            'industry',
            'retrieve_image',
            'routing',
            'knowledge_base',
            'is_active',
        ).first()

        routing_chain = RoutingChain.objects.get(id=bot_id)
        print(routing_chain)
        line_connection = LineConnectionNew.objects.filter(bot_id=routing_chain).values('uuid').first()
        print(line_connection)

        formatted_data = {
            'id': item['id'],
            'img': '',
            'bot_name': item['bot_name'],
            'routing': item['routing'],
            'prompt': item['prompt'],
            'industry': item['industry'],
            'retrieve_image': item['retrieve_image'],
            'knowledge_base': item['knowledge_base'],
            'isActive': item['is_active'],
            'line_integration_uuid': line_connection['uuid'] if line_connection else None,
        }
        return JsonResponse(formatted_data, status=200)


def edit_bot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bot_id = data.get('id')
        bot_name = data.get('bot_name')
        routing = data.get('routing')
        prompt = data.get('prompt')
        industry = data.get('industry')
        retrieve_image = data.get('retrieve_image')
        knowledge_base = data.get('knowledge_base')
        is_active = data.get('isActive')
        line_integration_uuid = data.get('line_integration_uuid')

        routing_chain = RoutingChain.objects.filter(id=bot_id).first()

        routing_chain.bot_name = bot_name
        routing_chain.routing = routing
        routing_chain.prompt = prompt
        routing_chain.industry = industry
        routing_chain.retrieve_image = retrieve_image
        routing_chain.knowledge_base = knowledge_base
        routing_chain.is_active = is_active
        routing_chain.save()

        routing_chain = RoutingChain.objects.get(id=bot_id)
        line_connection = LineConnectionNew.objects.filter(bot_id=routing_chain).first()
        if line_connection is None:
            print('Line connection is None')
            line_connection = LineConnectionNew.objects.create(
                bot_id=routing_chain,
                uuid=None,
            )

        line_integration = LineIntegration.objects.filter(uuid=line_integration_uuid).first()

        if line_connection:
            line_connection.uuid = line_integration
            line_connection.save()

        return JsonResponse({"message": "Done"}, status=200)
    
    
@csrf_exempt
def add_line_chatbot(request): 
    if request.method == 'POST':
        data = json.loads(request.body)

        user = request.user
        line_username = data.get('line_username')
        channel_id = data.get('channel_id') 
        secret_id = data.get('secret_id')
        
        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization
        
        line_chatbot_api_key = generate_access_key(channel_id, secret_id)
            
        # Add user before send message
        new_line_user = LineIntegration.objects.create(
            user_id=channel_id, 
            username=line_username, 
            line_chatbot_api_key=line_chatbot_api_key, 
            line_channel_secret=secret_id, 
            organization=organization
        )
        
        # Add webhook with respect to line user
        line_integration = LineIntegration.objects.get(user_id=channel_id, username=line_username)
        uuid = line_integration.uuid
        uuid = str(uuid)
        response = connect_line_webhook(line_chatbot_api_key, uuid)
        
        return JsonResponse({"message": "Done"}, status=200)
    elif request.method == 'GET':
        user = request.user
        line_username = 'test_user'
        channel_id = '2006620546'
        secret_id = "f6723362faba094ffe0a81c34e3af23c"

        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization

        line_chatbot_api_key = generate_access_key(channel_id, secret_id)

        # Add user before send message
        new_line_user = LineIntegration.objects.create(
            user_id=channel_id,
            username=line_username,
            line_chatbot_api_key=line_chatbot_api_key,
            line_channel_secret=secret_id,
            organization=organization
        )

        # Add webhook with respect to line user
        line_integration = LineIntegration.objects.get(user_id=channel_id, username=line_username)
        uuid = line_integration.uuid
        uuid = str(uuid)
        response = connect_line_webhook(line_chatbot_api_key, uuid)

        return JsonResponse({"message": "Done"}, status=200)

def request_demo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        company = data.get('company')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        new_request_demo = RequestDemo.objects.create(name=name, company=company, email=email, phone=phone, message=message)

        return JsonResponse({"message": "Done"}, status=200)
    

def list_channel_management(request):
    if request.method == 'GET':
        user = request.user
        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization

        # Get all LineIntegration records for this organization
        line_integrations = LineIntegration.objects.filter(organization_id=organization)
        
        formatted_messages = [
            {
                'id': line_integration.uuid,
                'img': '',
                'accountName': line_integration.username,
                'type': 'messenger', 
                'connectedBy': 'developer_test', 
                'connectedOn': line_integration.connected_on.strftime("%Y-%m-%d %H:%M:%S%z") if line_integration.connected_on else None
            }
            for line_integration in line_integrations
        ]

        return JsonResponse(formatted_messages, safe=False)

def count_bot_message(request):
    if request.method == 'GET':
        user = request.user
        organization_member = OrganizationMember.objects.filter(user=user).first()
        organization = organization_member.organization

        result = dict()

        messages_grouped = Message.objects.filter(by='bot',organization_id=organization) \
            .select_related('platform_id') \
            .values('organization_id', 'platform_id', 'platform_id__provider') \
            .annotate(message_count=Count('id'))

        agent_console_results = []
        for message_group in messages_grouped:
            print(f"Organization ID: {message_group['organization_id']}, "
                  f"Platform ID: {message_group['platform_id']}, "
                  f"Provider: {message_group['platform_id__provider']}, "
                  f"Message Count: {message_group['message_count']}")
            agent_console_results.append(message_group)

        result['agent_console'] = agent_console_results

        internal_chat_messages_grouped = InternalChatMessage.objects.filter(by='bot',organization_id=organization) \
            .select_related('bot_id') \
            .values('organization_id', 'bot_id__bot_name', 'user') \
            .annotate(message_count=Count('id'))

        internal_chat_results = []
        for message_group in internal_chat_messages_grouped:
            print(f"Organization ID: {message_group['organization_id']}, "
                  f"Bot Name: {message_group['bot_id__bot_name']}, "
                  f"User ID: {message_group['user']}, "
                  f"Message Count: {message_group['message_count']}")
            internal_chat_results.append(message_group)

        result['internal_chat'] = internal_chat_results

        return JsonResponse(result, status=200)


def download_s3_file(request):
    if request.method == 'GET':
        load_dotenv()

        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        try:
            file_key = '1 - Demo/TYFOOJYIGVDJFOVH7ULZZWXIYE/20250221_4PlusHospital.pdf'
            file_obj = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_key)

            file_data = file_obj['Body'].read()

            file_extension = file_key.split('.')[-1].lower()
            mime_type, _ = mimetypes.guess_type(file_key)

            # If MIME type is not detected, default to binary stream
            if not mime_type:
                mime_type = "application/octet-stream"

            # Set the response headers with the appropriate MIME type
            response = HttpResponse(file_data, content_type=mime_type)

            # Set the Content-Disposition header to prompt a download with the correct file name
            response['Content-Disposition'] = f'attachment; filename={file_key.split("/")[-1]}'

            return response

        except s3.exceptions.NoCredentialsError:
            return HttpResponse("AWS credentials not found.", status=403)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)


def serve_image(request):
    # Initialize boto3 client to access S3 (if the image is stored on S3)
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    try:
        # Decode the file path (handle URL-encoded file names)
        decoded_file_path = '1 - Demo/X2PJNU3OXJH5VPK23VJOVAWY3U/paragon_festival.jpg'

        # Fetch the image from S3 (or from the local directory if needed)
        file_obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=decoded_file_path)
        file_data = file_obj['Body'].read()

        # Get the MIME type of the image file based on its extension (e.g., .jpg, .png)
        mime_type, _ = mimetypes.guess_type(decoded_file_path)

        # If MIME type is not detected, set it to a default (fallback to binary stream)
        if not mime_type:
            mime_type = "application/octet-stream"

        # Respond with the image data and appropriate content type
        response = HttpResponse(file_data, content_type=mime_type)
        return response

    except s3.exceptions.NoCredentialsError:
        return HttpResponse("AWS credentials not found.", status=403)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
