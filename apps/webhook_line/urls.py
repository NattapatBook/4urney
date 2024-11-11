from django.urls import path
from apps.webhook_line.views import webhook

urlpatterns = [
    path('webhook/<uuid>/', webhook),
]