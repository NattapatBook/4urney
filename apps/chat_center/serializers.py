import datetime

from rest_framework import serializers

from apps.chat_center.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    case_count = serializers.IntegerField(read_only=True)
    double_case_count = serializers.SerializerMethodField()
    triple_case_count = serializers.IntegerField(read_only=True, default=-1)
    timestamp = serializers.SerializerMethodField()

    def get_double_case_count(self, instance):
        return instance.case_count * 2

    def get_timestamp(self, instance):
        return datetime.datetime.now()

    class Meta:
        model = Customer
        # fields = serializers.ALL_FIELDS
        exclude = ['image_url']
        read_only_fields = ['latest_message']
        extra_kwargs = dict(
            platform_uid=dict(
                required=False,
            )
        )