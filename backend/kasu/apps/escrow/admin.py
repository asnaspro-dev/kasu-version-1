from django.contrib import admin
from .models import EscrowTransaction


@admin.register(EscrowTransaction)
class EscrowTransactionAdmin(admin.ModelAdmin):
    list_display = ["order", "gross_amount", "net_amount", "release_status", "released_at"]
    list_filter = ["release_status"]
    raw_id_fields = ["order"]
