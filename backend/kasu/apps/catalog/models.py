"""
Modèles pour l'app catalog.
Catégories et produits publiés par les transitaires.
"""
from decimal import Decimal

from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Catégorie de produits.
    Ex: Électronique, Textile, Alimentaire...
    """

    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_category"
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Produit publié par un transitaire.
    Un même produit (même nom/sku) peut être proposé par plusieurs transitaires.
    """

    transitaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField("Nom du produit", max_length=255)
    description = models.TextField("Description", blank=True)
    unit = models.CharField(
        "Unité",
        max_length=20,
        default="pièce",
        help_text="Ex: pièce, kg, carton, lot...",
    )
    unit_price = models.DecimalField(
        "Prix unitaire",
        max_digits=12,
        decimal_places=2,
    )
    moq = models.PositiveIntegerField(
        "Quantité minimum de commande (MOQ)",
        default=1,
    )
    max_quantity = models.PositiveIntegerField(
        "Quantité maximale par commande",
        help_text="0 = pas de limite",
    )
    estimated_delivery_days = models.PositiveIntegerField(
        "Délai de livraison estimé (jours)",
        default=7,
    )
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_product"
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["transitaire"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.transitaire.email})"
