from django.contrib import admin
from .models import BoutiqueProfile


@admin.register(BoutiqueProfile)
class BoutiqueProfileAdmin(admin.ModelAdmin):
    list_display = ["shop_name", "user", "city", "country"]
    search_fields = ["shop_name", "user__email"]
    raw_id_fields = ["user"]
