"""
Modèles pour l'app transitaire.
Profil transitaire avec statut actif/archivé.
"""
from django.conf import settings
from django.db import models


class TransitaireStatus(models.TextChoices):
    """Statut du transitaire."""

    ACTIVE = "active", "Actif"
    ARCHIVED = "archived", "Archivé"


class TransitaireProfile(models.Model):
    """
    Profil étendu d'un transitaire.
    Un transitaire archivé ne peut plus publier de produits ni recevoir de commandes.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transitaire_profile",
    )
    company_name = models.CharField("Nom de l'entreprise", max_length=255)
    status = models.CharField(
        max_length=20,
        choices=TransitaireStatus.choices,
        default=TransitaireStatus.ACTIVE,
    )
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transitaire_profile"
        verbose_name = "Profil transitaire"
        verbose_name_plural = "Profils transitaires"
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"
