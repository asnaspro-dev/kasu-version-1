"""
Modèles pour l'app payments.
Paiements Mobile Money.
"""
from decimal import Decimal

from django.db import models

from apps.orders.models import Order


class PaymentProvider(models.TextChoices):
    """Fournisseurs de paiement Mobile Money."""

    MTN = "mtn", "MTN Mobile Money"
    ORANGE = "orange", "Orange Money"
    # Extensible
    OTHER = "other", "Autre"


class PaymentStatus(models.TextChoices):
    """Statuts d'un paiement."""

    PENDING = "pending", "En attente"
    COMPLETED = "completed", "Complété"
    FAILED = "failed", "Échoué"
    CANCELLED = "cancelled", "Annulé"


class Payment(models.Model):
    """
    Paiement lié à une commande.
    En V1 : Mobile Money uniquement.
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="payment",
    )
    amount = models.DecimalField(
        "Montant",
        max_digits=12,
        decimal_places=2,
    )
    provider = models.CharField(
        max_length=20,
        choices=PaymentProvider.choices,
    )
    transaction_reference = models.CharField(
        "Référence transaction",
        max_length=100,
        blank=True,
    )
    phone_number = models.CharField(
        "Numéro Mobile Money",
        max_length=20,
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments_payment"
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["status"]),
            models.Index(fields=["transaction_reference"]),
        ]

    def __str__(self):
        return f"Paiement {self.order.order_number} - {self.amount} ({self.status})"
