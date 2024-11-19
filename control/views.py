from pprint import pprint
from django.http import JsonResponse

import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

COGNITO_DOMAIN = settings.ENV('COGNITO_DOMAIN', default='')
COGNITO_APP_CLIENT_ID = settings.ENV('COGNITO_APP_CLIENT_ID', default='')
COGNITO_APP_CLIENT_SECRET = settings.ENV('COGNITO_APP_CLIENT_SECRET', default='')
COGNITO_REDIRECT_URL = (
        (f'https://{settings.HOST_NAME}' if settings.HOST_NAME else 'http://localhost:8000') +
        '/api/control/redirect/'
)


def login_view(request):
    # Redirect the user to the Cognito Hosted UI for authentication

    auth_url = (
        f"https://{COGNITO_DOMAIN}/login?"
        f"response_type=code&client_id={COGNITO_APP_CLIENT_ID}&"
        f"redirect_uri={COGNITO_REDIRECT_URL}"
    )
    return HttpResponseRedirect(auth_url)


def redirect_view(request):
    # Retrieve the authorization code from the callback request
    code = request.GET.get('code')
    if code:
        # Exchange the code for tokens (access token, ID token, refresh token)
        token_url = f"https://{COGNITO_DOMAIN}/oauth2/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': COGNITO_APP_CLIENT_ID,
            'client_secret': COGNITO_APP_CLIENT_SECRET,
            'code': code,
            'redirect_uri': COGNITO_REDIRECT_URL,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(token_url, data=data, headers=headers)

        if response.status_code == 200:
            tokens = response.json()
            # print(tokens.get('access_token'))
            request.session['access_token'] = tokens.get('access_token')
            request.session['id_token'] = tokens.get('id_token')
            request.session['refresh_token'] = tokens.get('refresh_token')

            # (Example - simplified user creation)
            user_response = requests.get(
                f'https://{COGNITO_DOMAIN}/oauth2/userInfo',
                headers=dict(Authorization=f'Bearer {tokens["access_token"]}')
            )
            if user_response.ok:
                user_info = user_response.json()
                user = User.objects.get_or_create(username=user_info['email'], defaults=dict(email=user_info['email']))[0]
                login(request, user)
                return HttpResponseRedirect('/api/control/test')

        else:
            pprint(response.json())

    return login_view(request)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def test_session(request):
    user_info = dict()
    access_token = request.session.get('access_token')
    id_token = request.session.get('id_token')
    refresh_token = request.session.get('refresh_token')

    if access_token:
        user_info_response = requests.get(
            f'https://{COGNITO_DOMAIN}/oauth2/userInfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        if user_info_response.ok:
            user_info = user_info_response.json()
        else:
            pass
    return JsonResponse(user_info)