"""
Serializers pour l'app delivery.
"""
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import Delivery, DeliveryStatus


class DeliverySerializer(serializers.ModelSerializer):
    """Serializer pour les livraisons."""

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    assigned_transitaire = UserPublicSerializer(read_only=True)
    status = serializers.ChoiceField(choices=DeliveryStatus.choices, read_only=True)

    class Meta:
        model = Delivery
        fields = [
            "id",
            "order",
            "order_number",
            "assigned_transitaire",
            "started_at",
            "delivered_at",
            "validated_by_boutique_at",
            "notes",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "order",
            "assigned_transitaire",
            "started_at",
            "delivered_at",
            "validated_by_boutique_at",
            "status",
            "created_at",
            "updated_at",
        ]


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mise à jour partielle (notes, statut par transitaire)."""

    class Meta:
        model = Delivery
        fields = ["notes"]


class DeliveryValidateSerializer(serializers.Serializer):
    """Serializer pour validation de livraison par la boutique."""

    notes = serializers.CharField(required=False, allow_blank=True)
