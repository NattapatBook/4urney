from django.contrib import admin

from apps.webhook_line.models import LineIntegration, LineConnection, LineConnectionNew

# Register your models here.

admin.site.register(LineIntegration)
admin.site.register(LineConnection)
admin.site.register(LineConnectionNew)