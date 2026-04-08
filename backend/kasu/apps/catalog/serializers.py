"""
Serializers pour l'app catalog.
Catégories et produits.
"""
from decimal import Decimal

from rest_framework import serializers

from apps.transitaire.serializers import TransitairePublicSerializer

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer pour les catégories."""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CategoryListSerializer(serializers.ModelSerializer):
    """Serializer léger pour listes."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer complet pour les produits (lecture)."""

    transitaire = TransitairePublicSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "transitaire",
            "category",
            "name",
            "description",
            "unit",
            "unit_price",
            "moq",
            "max_quantity",
            "estimated_delivery_days",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductWriteSerializer(serializers.ModelSerializer):
    """Serializer pour création/mise à jour de produits (transitaire)."""

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "unit",
            "unit_price",
            "moq",
            "max_quantity",
            "estimated_delivery_days",
            "is_active",
        ]

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le prix unitaire doit être strictement positif.")
        return value

    def validate_moq(self, value):
        if value < 1:
            raise serializers.ValidationError("Le MOQ doit être au moins 1.")
        return value

    def validate(self, attrs):
        moq = attrs.get("moq", 1)
        max_quantity = attrs.get("max_quantity", 0)
        if max_quantity > 0 and max_quantity < moq:
            raise serializers.ValidationError(
                {"max_quantity": "La quantité maximale doit être >= MOQ."}
            )
        return attrs
