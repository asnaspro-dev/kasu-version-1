"""
Serializers pour l'app payments.
"""
from rest_framework import serializers

from .models import Payment, PaymentProvider, PaymentStatus


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer pour les paiements."""

    order_number = serializers.CharField(source="order.order_number", read_only=True)
    status = serializers.ChoiceField(choices=PaymentStatus.choices, read_only=True)
    provider = serializers.ChoiceField(choices=PaymentProvider.choices)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "order_number",
            "amount",
            "provider",
            "transaction_reference",
            "phone_number",
            "status",
            "paid_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "amount",
            "status",
            "paid_at",
            "created_at",
            "updated_at",
        ]


class PaymentInitSerializer(serializers.Serializer):
    """
    Serializer pour initier un paiement Mobile Money.
    Le frontend envoie order_id, provider, phone_number.
    """

    order_id = serializers.IntegerField()
    provider = serializers.ChoiceField(choices=PaymentProvider.choices)
    phone_number = serializers.CharField(max_length=20)
