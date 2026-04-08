from django.contrib import admin
from .models import TrafficLog, Threat, Alert, AIModelRecord, UserActionLog

admin.site.register(TrafficLog)
admin.site.register(Threat)
admin.site.register(Alert)
admin.site.register(AIModelRecord)
admin.site.register(UserActionLog)
