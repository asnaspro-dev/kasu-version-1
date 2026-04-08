from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["order", "amount", "provider", "status", "paid_at"]
    list_filter = ["provider", "status"]
    search_fields = ["transaction_reference", "phone_number"]
    raw_id_fields = ["order"]
