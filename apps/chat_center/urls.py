from django.urls import path
from rest_framework.routers import DefaultRouter

# from apps.chat_center.views import my_api, CustomerViewSet
from apps.chat_center.views import list_user, list_message, admin_reply_post, change_message_type, list_user_test, \
    list_dashboard, get_user_detail, list_message_test, admin_reply_post_test, change_message_type_test, \
    list_dashboard_test, FileUploadView, create_bot, list_line_integration, list_industry_choices, summarize_dashboard, EmbeddedDataView, TaskStatusView, list_upload_file, list_knowledge_base

# router = DefaultRouter()
# router.register('customer', CustomerViewSet)

urlpatterns = [
    # path('my_api/', my_api),
    path('list_user/', list_user),
    path('list_user_test/', list_user_test),
    path('list_message/<user_id>', list_message),
    path('list_message_test/<user_id>', list_message_test),
    path('admin_reply_post/', admin_reply_post),
    path('admin_reply_post_test/', admin_reply_post_test),
    path('change_message_type/', change_message_type),
    path('change_message_type_test/', change_message_type_test),
    path('list_dashboard/<id>', list_dashboard),
    path('list_dashboard_test/<id>', list_dashboard_test),
    path('get_user/', get_user_detail),
    path('uploadTest/', FileUploadView.as_view(), name='file-upload'),
    path('create_bot/', create_bot),
    path('list_line_integration/', list_line_integration),
    path('list_industry/', list_industry_choices),
    path('summarize_dashboard/<user_id>', summarize_dashboard),
    path('embedded_data/', EmbeddedDataView.as_view(), name='embedded_data'),
    path('task_status/', TaskStatusView.as_view(), name='task_status'),
    path('list_upload_file/', list_upload_file),
    path('list_knowledge_base/', list_knowledge_base)
    # *router.urls,
]