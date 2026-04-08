"""
Modèles pour l'app delivery.
Livraisons et validation par la boutique.
"""
from django.conf import settings
from django.db import models

from apps.orders.models import Order


class DeliveryStatus(models.TextChoices):
    """Statuts d'une livraison."""

    PENDING = "pending", "En attente"
    IN_PROGRESS = "in_progress", "En cours"
    DELIVERED = "delivered", "Livré"
    VALIDATED = "validated", "Validé par la boutique"


class Delivery(models.Model):
    """
    Livraison liée à une commande.
    Le transitaire assigné est généralement celui de la commande.
    """

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="delivery",
    )
    assigned_transitaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="deliveries",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    validated_by_boutique_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "delivery_delivery"
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["assigned_transitaire"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Livraison {self.order.order_number} - {self.status}"
