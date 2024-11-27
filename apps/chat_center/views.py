from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render
import os
import psycopg2
import json
import sys
import requests
import pytz
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from apps.chat_center.models import User, OrganizationMember

DB_CONFIG = {
    'host': os.environ.get('DEMO_DATABASE_HOST'),
    'database': os.environ.get('DEMO_DATABASE_NAME'),
    'user': os.environ.get('DEMO_DATABASE_USER'),
    'password': os.environ.get('DEMO_DATABASE_PASSWORD'),
    'port': os.environ.get('DEMO_DATABASE_PORT'),
}

LINE_CHATBOT_API_KEY = os.environ.get('LINE_CHATBOT_API_KEY')
LINE_API = 'https://api.line.me/v2/bot/message/reply'

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
    users = User.objects.all()
    data = serialize('json', users)
    return JsonResponse(data, safe=False)

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
