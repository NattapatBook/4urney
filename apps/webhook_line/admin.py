from django.contrib import admin

from apps.webhook_line.models import LineIntegration, LineConnection

# Register your models here.

admin.site.register(LineIntegration)
admin.site.register(LineConnection)