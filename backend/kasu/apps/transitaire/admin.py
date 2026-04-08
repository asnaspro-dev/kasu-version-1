from django.contrib import admin
from .models import TransitaireProfile


@admin.register(TransitaireProfile)
class TransitaireProfileAdmin(admin.ModelAdmin):
    list_display = ["company_name", "user", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["company_name", "user__email"]
    raw_id_fields = ["user"]
