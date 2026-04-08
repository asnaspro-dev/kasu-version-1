from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "transitaire", "category", "unit_price", "moq", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]
    raw_id_fields = ["transitaire", "category"]
