import uuid
from django.db import models


class LineIntegration(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    line_chatbot_api_key = models.CharField(max_length=255)
    line_channel_secret = models.CharField(max_length=255)
    organization = models.ForeignKey('chat_center.Organization', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.user_id}"
