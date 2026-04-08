"""
Modèles pour l'app notifications.
Notifications in-app pour les utilisateurs.
"""
from django.conf import settings
from django.db import models


class NotificationType(models.TextChoices):
    """Types de notifications."""

    ORDER_PLACED = "order_placed", "Commande passée"
    PAYMENT_RECEIVED = "payment_received", "Paiement reçu"
    DELIVERY_STARTED = "delivery_started", "Livraison en cours"
    DELIVERY_VALIDATED = "delivery_validated", "Livraison validée"
    SYSTEM = "system", "Système"


class Notification(models.Model):
    """
    Notification destinée à un utilisateur.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
    )
    title = models.CharField("Titre", max_length=255)
    message = models.TextField("Message")
    link = models.URLField(blank=True, help_text="Lien associé (optionnel)")
    is_read = models.BooleanField("Lu", default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications_notification"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"
