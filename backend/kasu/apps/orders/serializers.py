"""
Serializers pour l'app orders.
Commandes et lignes de commande.
"""
from decimal import Decimal

from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer
from apps.catalog.models import Product
from apps.transitaire.serializers import TransitairePublicSerializer

from .models import Order, OrderItem, OrderStatus


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer pour une ligne de commande."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_unit = serializers.CharField(source="product.unit", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_unit",
            "quantity",
            "unit_price",
            "line_total",
        ]
        read_only_fields = ["unit_price", "line_total"]


class OrderItemWriteSerializer(serializers.Serializer):
    """Serializer pour création de ligne de commande."""

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        try:
            Product.objects.get(pk=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produit introuvable ou inactif.")
        return value

    def validate_quantity(self, value):
        product = Product.objects.get(pk=self.initial_data.get("product_id"))
        if value < product.moq:
            raise serializers.ValidationError(
                f"La quantité minimale est {product.moq} (MOQ)."
            )
        if product.max_quantity > 0 and value > product.max_quantity:
            raise serializers.ValidationError(
                f"La quantité maximale est {product.max_quantity}."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    """Serializer complet pour les commandes (lecture)."""

    boutique = UserPublicSerializer(read_only=True)
    transitaire = TransitairePublicSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(choices=OrderStatus.choices, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "boutique",
            "transitaire",
            "total_amount",
            "commission_rate",
            "commission_amount",
            "net_amount",
            "delivery_address",
            "delivery_latitude",
            "delivery_longitude",
            "status",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "total_amount",
            "commission_rate",
            "commission_amount",
            "net_amount",
            "status",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer pour création de commande.
    items: [{ product_id, quantity }, ...]
    Tous les produits doivent appartenir au même transitaire.
    """

    items = OrderItemWriteSerializer(many=True)
    delivery_address = serializers.CharField()
    delivery_latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
    )
    delivery_longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
    )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Au moins un produit est requis.")
        return value
