import uuid
from django.db import models

class INDUSTRY(models.TextChoices):
    AGRICULTURE = 'AGRICULTURE'
    HR = 'HR'


class LineIntegration(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    line_chatbot_api_key = models.CharField(max_length=255)
    line_channel_secret = models.CharField(max_length=255)
    organization = models.ForeignKey('chat_center.Organization', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.user_id}"
    

class RoutingChain(models.Model):
    bot_name = models.CharField(max_length=255)
    routing = models.CharField(max_length=255)
    prompt = models.TextField(null=True, blank=True)
    industry = models.CharField(choices=INDUSTRY.choices, max_length=100)
    retrieve_image = models.BooleanField(null=True, blank=True)
    knowledge_base = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.ForeignKey(LineIntegration, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bot Name: {self.bot_name} KB: {self.knowledge_base}"