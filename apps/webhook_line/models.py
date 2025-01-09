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
        return f"{self.uuid}"
    

class LineConnection(models.Model):
    bot_id = models.ForeignKey('chat_center.RoutingChain', to_field="id", on_delete=models.CASCADE,null=True, blank=True)
    uuid = models.ForeignKey(LineIntegration, to_field="uuid", on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.bot_id} - {self.uuid}"