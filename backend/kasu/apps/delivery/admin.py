from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ["order", "assigned_transitaire", "status", "delivered_at"]
    list_filter = ["status"]
    raw_id_fields = ["order", "assigned_transitaire"]
