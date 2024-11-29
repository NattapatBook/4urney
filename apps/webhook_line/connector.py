import json
import requests

async def reply_message(user_id, reply_token, text_message, line_access_token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = f'Bearer {line_access_token}'

    headers = {
        # 'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": text_message
        }]
    }
    # data = json.dumps(data)
    response = requests.post(LINE_API, headers=headers, json=data)

    return response.status_code


def get_username(user_id, line_access_token):
    Authorization = f'Bearer {line_access_token}'

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    x = requests.get(url=f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
    x_content_dict = x.json()

    # Access the desired key
    username = x_content_dict['displayName']
    return username