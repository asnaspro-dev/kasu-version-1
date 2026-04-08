from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "role", "is_active", "created_at"]
    list_filter = ["role", "is_active"]
    search_fields = ["email", "phone_number"]
    ordering = ["-created_at"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("KASU", {"fields": ("role", "phone_number", "is_verified")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("KASU", {"fields": ("email", "role", "phone_number")}),
    )
