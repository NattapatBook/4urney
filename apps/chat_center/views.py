import csv

from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import psycopg2
import json
import requests
import pytz
from datetime import datetime
from channels.layers import get_channel_layer

from rest_framework import status, permissions
from rest_framework.permissions import AllowAny

from apps.chat_center.models import User, OrganizationMember, Customer, Message, Dashboard, UploadedFile
from apps.webhook_line.models import LineIntegration
from apps.chat_center.serializers import FileUploadSerializer
from rest_framework.views import APIView

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
    # Fetch the dashboard data (assuming you're querying a single record, e.g., the one with id="-1")
    try:
        dashboard = Dashboard.objects.get(platform_id=id)
    except Dashboard.DoesNotExist:
        return JsonResponse({"error": "Dashboard not found"}, status=400)

    response_data = {
        "dissatisfaction": dashboard.dissatisfaction if dashboard.dissatisfaction is not None else 0,
        "intentSummary": eval(dashboard.intentsummary) if dashboard.intentsummary else [],
        "priority": dashboard.priority if dashboard.priority else None,
        "satisfaction": dashboard.satisfaction if dashboard.satisfaction is not None else 0,
        "totalMessage": dashboard.totalmessage if dashboard.totalmessage is not None else 0,
        "totalSession": dashboard.totalsession if dashboard.totalsession is not None else 0,
        "urgent": dashboard.urgent if dashboard.urgent is not None else 0,
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
    queryset = UploadedFile.objects.all()  # Modify as needed

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.save()

            print(f"Uploaded file name: {uploaded_file.file.name}")
            print(f"File stored at: {uploaded_file.file.url}")

            if uploaded_file.file.name.endswith('.csv'):
                try:
                    with open(uploaded_file.file.path, mode='r', newline='', encoding='utf-8') as file:
                        csv_reader = csv.DictReader(file)
                        rows = list(csv_reader)

                        data = rows[:5]
                        print(data)

                        return JsonResponse({"message": "File uploaded and processed successfully!", "data": data},
                                            status=200)
                except Exception as e:
                    return JsonResponse({"message": "Failed to read the CSV file", "error": str(e)}, status=400)

            return JsonResponse({"message": "Uploaded file is not a CSV"}, status=400)

        return JsonResponse({"message": "File upload failed", "errors": serializer.errors}, status=400)

# class FileUploadView(APIView):
#     queryset = UploadedFile.objects.all()  # Modify as needed
#
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         # Serialize the uploaded file
#         serializer = FileUploadSerializer(data=request.data)
#
#         if serializer.is_valid():
#             uploaded_file = serializer.save()
#
#             # Rename the file before saving
#             if uploaded_file.file:
#                 file_path = uploaded_file.file.path
#                 base_name, extension = os.path.splitext(uploaded_file.file.name)
#
#                 # Define your new file name logic here
#                 new_file_name = f"test_upload_file{extension}"
#
#                 # Construct the new file path
#                 new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
#
#                 # Rename the file
#                 os.rename(file_path, new_file_path)
#
#                 # Update the file path in the model
#                 uploaded_file.file.name = os.path.join('uploads', new_file_name)  # Adjust as needed for your file path logic
#                 uploaded_file.save()
#
#             # Read the CSV file after saving it
#             if uploaded_file.file.name.endswith('.csv'):
#                 try:
#                     # Open the uploaded CSV file and read its content
#                     with open(uploaded_file.file.path, mode='r', newline='', encoding='utf-8') as file:
#                         csv_reader = csv.DictReader(file)  # This assumes the CSV has a header row
#                         rows = list(csv_reader)  # Convert the CSV content to a list of dictionaries
#
#                         # Process the CSV content as needed
#                         # For demonstration, let's just return the first 5 rows
#                         data = rows[:5]
#                         print(data)
#
#                         return JsonResponse({"message": "File uploaded, renamed, and processed successfully!", "data": data},
#                                             status=200)
#                 except Exception as e:
#                     return JsonResponse({"message": "Failed to read the CSV file", "error": str(e)}, status=400)
#
#             return JsonResponse({"message": "Uploaded file is not a CSV"}, status=400)
#
#         return JsonResponse({"message": "File upload failed", "errors": serializer.errors}, status=400)