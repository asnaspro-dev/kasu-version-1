from django.contrib import admin
from .models import SystemSetting, AuditLog


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "value_type", "description"]
    search_fields = ["key"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "created_at"]
    list_filter = ["action"]
    readonly_fields = ["user", "action", "model_name", "object_id", "details", "ip_address", "created_at"]
    search_fields = ["action", "model_name"]
