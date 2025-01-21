import datetime
import os

from django.core.files.utils import validate_file_name
from rest_framework import serializers

from apps.chat_center.models import Customer, UploadedFile


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

class FileUploadSerializer(serializers.Serializer):
    file = serializers.CharField()
    # class Meta:
    #     model = UploadedFile
    #     fields = ['file']

    def validate_file(self, value):
        try:
            validate_file_name(os.path.basename(value))
            return value
        except:
            raise serializers.ValidationError('invalid filename')

    def create(self, validated_data):
        organization_member = validated_data.pop('organization_member', None)
        validated_data["file"] = os.path.join(f'{organization_member.organization}',os.path.basename(validated_data["file"]))
        uploaded_file = UploadedFile.objects.create(organization_member=organization_member, **validated_data)
        return uploaded_file