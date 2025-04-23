from django.urls import path
from rest_framework.routers import DefaultRouter

# from apps.chat_center.views import my_api, CustomerViewSet
from apps.chat_center.views import get_user_detail, \
    FileUploadView, create_bot, list_line_integration, list_industry_choices, \
    EmbeddedDataView, TaskStatusView, list_upload_file, list_knowledge_base, list_bot, create_session, list_session, \
    rename_session, remove_session, get_internal_chat, internal_chatbot, remove_upload_file, edit_upload_file, \
    get_chatbot_data, edit_bot, add_line_chatbot, get_chatbot_data_new, request_demo, \
    list_channel_management, count_bot_message, download_s3_file, view_image, list_information_extraction_result, \
    search_engine, plotly_test2, list_user_new, \
    list_message_new, admin_reply_post_new, change_message_type_new, list_dashboard_new, edit_customer_profile_new, \
    summarize_dashboard_new, save_draft, list_bot_ai_management, chatbot_publish, remove_bot, list_save_draft_session, \
    chat_with_data

# router = DefaultRouter()
# router.register('customer', CustomerViewSet)

urlpatterns = [
    # path('my_api/', my_api),
    path('list_user_new/', list_user_new),
    path('list_message_new/<user_id>', list_message_new),
    path('admin_reply_post_new/', admin_reply_post_new),
    path('change_message_type_new/', change_message_type_new),
    path('list_dashboard_new/<id>', list_dashboard_new),
    path('edit_customer_profile_new/', edit_customer_profile_new),
    path('get_user/', get_user_detail),
    path('uploadTest/', FileUploadView.as_view(), name='file-upload'),
    path('create_bot/', create_bot),
    path('list_line_integration/', list_line_integration),
    path('list_industry/', list_industry_choices),
    path('list_knowledge_base/', list_knowledge_base),
    path('summarize_dashboard_new/<user_id>', summarize_dashboard_new),
    path('list_upload_file/', list_upload_file),
    path('remove_upload_file/', remove_upload_file),
    path('edit_upload_file/', edit_upload_file),
    path('embedded_data/', EmbeddedDataView.as_view(), name='embedded_data'),
    path('task_status/', TaskStatusView.as_view(), name='task_status'),
    path('list_bot/', list_bot),
    path('remove_bot/', remove_bot),
    path('create_session/', create_session),
    path('list_session/', list_session),
    path('list_save_draft_session/', list_save_draft_session), 
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
    path('view_image/', view_image), 
    path('list_information_extraction_result/', list_information_extraction_result),
    path('search_engine/', search_engine),
    path('plotly_test1/', plotly_test1),
    path('plotly_test2/', plotly_test2),
    path('plotly_test3/', plotly_test3),
    path('save_draft/', save_draft), 
    path('list_bot_ai_management/', list_bot_ai_management), 
    path('chatbot_publish/', chatbot_publish),
    path('chat_with_data/', chat_with_data),
    # *router.urls,
]