"""
Modèles pour l'app orders.
Commandes et lignes de commande.
"""
from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.catalog.models import Product


class OrderStatus(models.TextChoices):
    """Statuts d'une commande."""

    PENDING_PAYMENT = "pending_payment", "En attente de paiement"
    PAID = "paid", "Payée"
    IN_DELIVERY = "in_delivery", "En livraison"
    DELIVERED = "delivered", "Livrée"
    CANCELLED = "cancelled", "Annulée"


class Order(models.Model):
    """
    Commande passée par une boutique auprès d'un transitaire.
    Une commande est liée à un seul transitaire (tous les produits viennent de lui).
    """

    order_number = models.CharField("Numéro de commande", max_length=50, unique=True)
    boutique = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders_as_boutique",
    )
    transitaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders_as_transitaire",
    )
    total_amount = models.DecimalField(
        "Montant total",
        max_digits=12,
        decimal_places=2,
    )
    commission_rate = models.DecimalField(
        "Taux de commission (%)",
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
    delivery_address = models.TextField("Adresse de livraison")
    delivery_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    delivery_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING_PAYMENT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders_order"
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["boutique"]),
            models.Index(fields=["transitaire"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Commande {self.order_number} ({self.boutique.email})"


class OrderItem(models.Model):
    """
    Ligne de commande : un produit avec quantité et prix unitaire.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField("Quantité")
    unit_price = models.DecimalField(
        "Prix unitaire au moment de la commande",
        max_digits=12,
        decimal_places=2,
    )
    line_total = models.DecimalField(
        "Total ligne",
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "orders_orderitem"
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
        unique_together = [["order", "product"]]

    def __str__(self):
        return f"{self.product.name} x {self.quantity} - {self.order.order_number}"
