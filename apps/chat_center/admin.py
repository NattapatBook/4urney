from django.contrib import admin
from django.db.models import OuterRef, Count

from apps.chat_center.models import Organization, OrganizationMember, Customer, Message, Dashboard, UploadedFile, \
    RoutingChain \
    , ChatSummarize, ChatUserSatisfaction, ChatUserUrgent, InternalChatMessage, InternalChatSession, RoutingSkill, \
    FieldConnection \
    , InformationExtractionSkill, SkillConnection, RequestDemo, CustomerNew

# from apps.chat_center.models import Customer, Case, Topic, TopicHandler


# Register your models here.

admin.site.register(Organization)
admin.site.register(OrganizationMember)
admin.site.register(Customer)
admin.site.register(Message)
admin.site.register(Dashboard)
admin.site.register(UploadedFile)
admin.site.register(RoutingChain)
admin.site.register(ChatSummarize)
admin.site.register(ChatUserSatisfaction)
admin.site.register(ChatUserUrgent)
admin.site.register(InternalChatMessage)
admin.site.register(InternalChatSession)
admin.site.register(RoutingSkill)
admin.site.register(FieldConnection)
admin.site.register(InformationExtractionSkill)
admin.site.register(SkillConnection)
admin.site.register(RequestDemo)
admin.site.register(CustomerNew)

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['platform_uid', 'id', 'platform', 'platform_name', 'case_count']
#     list_display_links = ['platform_uid']
#     list_filter = ['platform']
#     search_fields = ['platform_name', 'platform_uid']
#
#     def case_count(self, instance):
#         return instance.case_count
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(
#             case_count=Case.objects.filter(
#                 customer=OuterRef('id')
#             ).values('customer').annotate(
#                 count=Count(1)
#             ).values('count')[:1]
#         )
#         return queryset
#
#
# admin.site.register(Customer, CustomerAdmin)
#
# # admin.site.register(
# #     Customer,
# #     list_display=['id', 'platform', 'platform_name', 'platform_uid'],
# #     list_display_links=['platform_uid'],
# #     list_filter=['platform'],
# #     search_fields=['platform_name', 'platform_uid'],
# # )
#
# admin.site.register(
#     Case,
#     list_display=['id', 'customer', 'topic', 'topic_handler', 'priority', 'created', 'closed', 'closed_by'],
#     search_fields=['customer__platform_name'],
# )
#
# admin.site.register(
#     Topic,
# )
#
# admin.site.register(
#     TopicHandler,
# )
