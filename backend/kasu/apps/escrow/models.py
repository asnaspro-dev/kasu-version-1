"""
Modèles pour l'app escrow.
Séquestre : garde des fonds jusqu'à validation livraison.
"""
from decimal import Decimal

from django.db import models

from apps.orders.models import Order


class EscrowReleaseStatus(models.TextChoices):
    """Statut de libération du séquestre."""

    LOCKED = "locked", "Bloqué"
    RELEASED = "released", "Libéré"


class EscrowTransaction(models.Model):
    """
    Transaction de séquestre liée à une commande.
    L'argent est bloqué jusqu'à validation de la livraison par la boutique.
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="escrow_transaction",
    )
    gross_amount = models.DecimalField(
        "Montant brut",
        max_digits=12,
        decimal_places=2,
    )
    commission_rate = models.DecimalField(
        "Taux commission (%)",
        max_digits=5,
        decimal_places=2,
    )
    commission_amount = models.DecimalField(
        "Montant commission",
        max_digits=12,
        decimal_places=2,
    )
    net_amount = models.DecimalField(
        "Montant net transitaire",
        max_digits=12,
        decimal_places=2,
    )
    release_status = models.CharField(
        max_length=20,
        choices=EscrowReleaseStatus.choices,
        default=EscrowReleaseStatus.LOCKED,
    )
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "escrow_transaction"
        verbose_name = "Transaction séquestre"
        verbose_name_plural = "Transactions séquestre"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["release_status"]),
        ]

    def __str__(self):
        return f"Escrow {self.order.order_number} - {self.release_status}"
