from django.urls import path
from rest_framework.routers import DefaultRouter

# from apps.chat_center.views import my_api, CustomerViewSet
from apps.chat_center.views import list_user, list_message, admin_reply_post, change_message_type, list_user_test

# router = DefaultRouter()
# router.register('customer', CustomerViewSet)

urlpatterns = [
    # path('my_api/', my_api),
    path('list_user/', list_user),
    path('list_user_test/', list_user_test),
    path('list_message/<user_id>', list_message),
    path('admin_reply_post/', admin_reply_post),
    path('change_message_type/', change_message_type),
    # *router.urls,
]