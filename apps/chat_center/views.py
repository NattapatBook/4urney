import json

from django.db.models import OuterRef, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from apps.chat_center.models import Customer, Case
from apps.chat_center.serializers import CustomerSerializer


# Create your views here.


def my_api(request):
    result = [
        {
            'platform': customer.platform,
            'platform_uid': customer.platform_uid,
            'platform_name': customer.platform_name,
            'image_url': customer.image_url if customer.image_url else None,
            'latest_message': customer.latest_message,
        }
        for customer in Customer.objects.all()
    ]
    return JsonResponse(result, safe=False)
    # return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # renderer_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            case_count=Case.objects.filter(
                customer=OuterRef('id')
            ).values('customer').annotate(
                count=Count(1)
            ).values('count')[:1]
        )
        return queryset

    def filter_queryset(self, queryset):
        if platform := self.request.query_params.get('platform'):
            queryset = queryset.filter(platform=platform)
        return queryset



