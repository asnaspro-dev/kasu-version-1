"""
Serializers pour l'app escrow.
"""
from rest_framework import serializers

from .models import EscrowTransaction, EscrowReleaseStatus


class EscrowTransactionSerializer(serializers.ModelSerializer):
    """Serializer pour les transactions de séquestre (lecture seule pour les clients)."""

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    release_status = serializers.ChoiceField(
        choices=EscrowReleaseStatus.choices,
        read_only=True,
    )

    class Meta:
        model = EscrowTransaction
        fields = [
            "id",
            "order",
            "order_number",
            "gross_amount",
            "commission_rate",
            "commission_amount",
            "net_amount",
            "release_status",
            "released_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
