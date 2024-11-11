from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.chat_center.views import my_api, CustomerViewSet

router = DefaultRouter()
router.register('customer', CustomerViewSet)

urlpatterns = [
    path('my_api/', my_api),
    *router.urls,
]