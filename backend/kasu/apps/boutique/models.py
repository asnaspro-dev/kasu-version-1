"""
Modèles pour l'app boutique.
Profil boutique avec adresse de livraison.
"""
from django.conf import settings
from django.db import models


class BoutiqueProfile(models.Model):
    """
    Profil étendu d'une boutique.
    Un User avec role=boutique peut avoir un BoutiqueProfile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boutique_profile",
    )
    shop_name = models.CharField("Nom de la boutique", max_length=255)
    address = models.TextField("Adresse complète")
    city = models.CharField("Ville", max_length=100)
    country = models.CharField("Pays", max_length=100, default="Cameroun")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude pour géolocalisation",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude pour géolocalisation",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "boutique_profile"
        verbose_name = "Profil boutique"
        verbose_name_plural = "Profils boutiques"
        indexes = [
            models.Index(fields=["city"]),
        ]

    def __str__(self):
        return f"{self.shop_name} ({self.user.email})"
