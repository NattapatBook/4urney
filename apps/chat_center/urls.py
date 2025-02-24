from django.urls import path
from rest_framework.routers import DefaultRouter

# from apps.chat_center.views import my_api, CustomerViewSet
from apps.chat_center.views import list_user, list_message, admin_reply_post, change_message_type, list_user_test, \
    list_dashboard, get_user_detail, list_message_test, admin_reply_post_test, change_message_type_test, \
    list_dashboard_test, FileUploadView, create_bot, list_line_integration, list_industry_choices, summarize_dashboard, \
    EmbeddedDataView, TaskStatusView, list_upload_file, list_knowledge_base, list_bot, create_session, list_session, \
    rename_session, remove_session, get_internal_chat, internal_chatbot, remove_upload_file, edit_upload_file, \
    edit_customer_profile, get_chatbot_data, edit_bot, add_line_chatbot, get_chatbot_data_new, request_demo, \
    list_channel_management, count_bot_message, download_s3_file, gview_image

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
    path('edit_customer_profile/', edit_customer_profile),
    path('get_user/', get_user_detail),
    path('uploadTest/', FileUploadView.as_view(), name='file-upload'),
    path('create_bot/', create_bot),
    path('list_line_integration/', list_line_integration),
    path('list_industry/', list_industry_choices),
    path('list_knowledge_base/', list_knowledge_base),
    path('summarize_dashboard/<user_id>', summarize_dashboard),
    path('list_upload_file/', list_upload_file),
    path('remove_upload_file/', remove_upload_file),
    path('edit_upload_file/', edit_upload_file),
    path('embedded_data/', EmbeddedDataView.as_view(), name='embedded_data'),
    path('task_status/', TaskStatusView.as_view(), name='task_status'),
    path('list_bot/', list_bot),
    path('create_session/', create_session),
    path('list_session/', list_session),
    path('rename_session/', rename_session),
    path('remove_session/', remove_session),
    path('get_internal_chat/', get_internal_chat),
    path('send_message_internal_chat/', internal_chatbot),
    path('get_chatbot_data/', get_chatbot_data),
    path('edit_bot/', edit_bot), 
    path('add_line_chatbot/', add_line_chatbot),
    path('get_chatbot_data_new/', get_chatbot_data_new),
    path('request_demo/', request_demo), 
    path('list_channel_management/', list_channel_management),
    path('count_bot_message/', count_bot_message),
    path('download_s3_file/', download_s3_file),
    path('view_image/', view_image)
    # *router.urls,
]