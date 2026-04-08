from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "boutique",
        "transitaire",
        "total_amount",
        "status",
        "created_at",
    ]
    list_filter = ["status"]
    search_fields = ["order_number", "boutique__email", "transitaire__email"]
    raw_id_fields = ["boutique", "transitaire"]
    inlines = [OrderItemInline]

