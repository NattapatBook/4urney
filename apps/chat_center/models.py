import datetime
import os

from django.contrib.auth.models import User, Group
from django.db import models
from datetime import datetime, timedelta

from django.db.models import Q

class INDUSTRY(models.TextChoices):
    AGRICULTURE = 'AGRICULTURE'
    HR = 'HR'

# Create your models here.
# class PLATFORM(models.TextChoices):
#     LINE = 'LINE'
#     FACEBOOK = 'FACEBOOK'
#
#
# class PRIORITY(models.IntegerChoices):
#     HIGH = 1
#     MEDIUM = 2
#     LOW = 3
#
#
# class Customer(models.Model):
#     platform = models.CharField(
#         choices=PLATFORM.choices, max_length=100
#     )
#     platform_uid = models.TextField()
#     platform_name = models.TextField(blank=True)
#     image_url = models.ImageField(null=True, blank=True)
#     latest_message = models.TextField(blank=True)
#     # latest_message = models.ForeignKey('Message', models.SET_NULL, null=True, blank=True)
#     # timestamp = models.DateTimeField()
#
#     def __str__(self):
#         return f'{self.platform} {self.platform_name}'
#
#     @property
#     def case_count(self):
#         if hasattr(self, '_case_count'):
#             return self._case_count or 0
#         return Case.objects.filter(customer=self).count()
#
#     @case_count.setter
#     def case_count(self, value):
#         self._case_count = value
#
# class Topic(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f'{self.name}'
#
# class TopicHandler(models.Model):
#     topic = models.ForeignKey(Topic, models.PROTECT, related_name='handlers')
#     index = models.IntegerField()
#     handler = models.ForeignKey(Group, models.PROTECT)
#
#     auto_escalate = models.DurationField(null=True, blank=True)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['topic', 'index'], name='topic_handler')
#         ]
#
#     def __str__(self):
#         return f'{self.handler}'
#
# class Case(models.Model):
#     customer = models.ForeignKey(Customer, models.PROTECT, related_name='cases')
#     topic = models.ForeignKey(Topic, models.PROTECT, related_name='cases')
#     topic_handler = models.ForeignKey(TopicHandler, models.PROTECT, related_name='cases')
#     priority = models.IntegerField(choices=PRIORITY.choices)
#
#
#     created = models.DateTimeField(auto_now_add=True)
#     closed = models.DateTimeField(null=True, blank=True)
#     closed_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True, blank=True)
#
#
# class Message(models.Model):
#     case = models.ForeignKey(Case, models.PROTECT, related_name='messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField()
#     is_from_customer = models.BooleanField()
#     # sent_by = models.TextField(blank=True)
#     sent_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True, blank=True)
#
#
# # schedule run every 1 minute
# def escalate_cases():
#     queryset = Case.objects.filter(
#         closed_by=None,
#     ).exclude(
#         topic_handler__auto_escalate=None,
#     ).annotate(
#         aging=models.ExpressionWrapper(
#             models.Value(datetime.datetime.now()) - models.F('created'),
#             # output_field=models.DurationField()
#         ),
#         auto_escalate=models.F('topic_handler__auto_escalate'),
#     ).filter(
#         aging__gte=models.F('auto_escalate'),
#     )
#
#     for case in queryset:
#         next_index = case.topic_handler.index + 1
#         next_handler = TopicHandler.objects.filter(
#             topic=case.topic,
#             index=next_index,
#         ).first()
#         if next_handler:
#             case.topic_handler = next_handler
#             case.save(update_fields=['topic_handler'])
#
#
# def count_by_platform():
#     queryset = Customer.objects.filter().values('platform').annotate(
#         count_by_platform=models.Count(1),
#     )
#     return queryset.filter(count_by_platform=1)
#
#     # return Customer.objects.filter().values('platform').aggregate(
#     #     count_by_platform=models.Count(1),
#     # )
#
#
# def noob():
#     queryset = Customer.objects.filter(
#         Q(platform=PLATFORM.LINE) | Q(platform_uid__startswith='u') | Q(platform_uid__endswith='x'),
#         latest_message__gt='',
#     ).order_by('platform_name').defer('image_url')
#
# def annotate_subquery():
#     customers = Customer.objects.all().annotate(
#         new_latest_message=Message.objects.filter(
#             case__customer__id=models.OuterRef('id')
#         ).order_by('-timestamp').values('content')[:1]
#     )
#
#     print(Message.objects.filter(case__customer__platform_name='A').order_by('-timestamp')[:1])
#
#     return customers
#
# def get_query_set():
#     customer = Customer.objects.filter().annotate(
#         case_count=Case.objects.filter(customer=models.OuterRef('id')).values('customer').annotate(case_count=models.Count(1)).values('case_count')[:1]
#     )

# class Role(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrganizationMember(models.Model):
    # username = models.CharField(max_length=255, unique=True)
    # email = models.EmailField()
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class Customer(models.Model):
    platform_id = models.CharField(max_length=1000, primary_key=True) # change pk use id
    img = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    tag = models.CharField(max_length=1000, null=True, blank=True)
    priority = models.CharField(max_length=1000, null=True, blank=True)
    lastest_msg = models.CharField(max_length=1000, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    is_urgent = models.BooleanField(null=True, blank=True)
    provider = models.CharField(max_length=1000, null=True, blank=True)
    agent = models.CharField(max_length=1000, null=True, blank=True)
    message_type = models.CharField(max_length=255, null=True, blank=True)
    reply_token = models.CharField(max_length=1000, null=True, blank=True)
    organization_id = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.platform_id})"

class Message(models.Model):
    platform_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    by = models.CharField(max_length=255, null=True, blank=True) # user or customer
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True) # user => admin(a,b,c) , bot(a,b,c)
    timestamp = models.DateTimeField(null=True, blank=True)
    organization_id = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.by} at {self.timestamp}"

class Dashboard(models.Model):
    platform_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    gender = models.CharField(max_length=1000, null=True, blank=True)
    phonenumber = models.CharField(max_length=1000, null=True, blank=True)
    citizenid = models.CharField(max_length=1000, null=True, blank=True)
    birthday = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    satisfaction = models.IntegerField(null=True, blank=True)
    dissatisfaction = models.IntegerField(null=True, blank=True)
    totalsession = models.IntegerField(null=True, blank=True)
    totalmessage = models.IntegerField(null=True, blank=True)
    urgent = models.IntegerField(null=True, blank=True)
    priority = models.CharField(max_length=1000, null=True, blank=True)
    intentsummary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else self.id


def file_upload_to(instance, filename):
    organization_member = instance.organization_member
    organization_name = organization_member.organization.name if organization_member else "default"

    return os.path.join(organization_name, filename)

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class RoutingChain(models.Model):
    bot_id = models.CharField(max_length=1000, primary_key=True)
    bot_name = models.CharField(max_length=255)
    routing = models.CharField(max_length=255)
    prompt = models.TextField(null=True, blank=True)
    industry = models.CharField(choices=INDUSTRY.choices, max_length=100)
    retrieve_image = models.BooleanField(null=True, blank=True)
    knowledge_base = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bot Name: {self.bot_name} KB: {self.knowledge_base}"