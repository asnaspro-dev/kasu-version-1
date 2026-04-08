"""
Modèles pour l'app accounts.
Custom User avec rôle (boutique, transitaire, admin).
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """Rôles utilisateur de la plateforme."""

    BOUTIQUE = "boutique", "Boutique"
    TRANSITAIRE = "transitaire", "Transitaire"
    ADMIN = "admin", "Administrateur"


class User(AbstractUser):
    """
    Utilisateur personnalisé avec email comme identifiant principal.
    Le champ username est conservé pour compatibilité mais email sert de login.
    """

    email = models.EmailField("Adresse email", unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.BOUTIQUE,
    )
    phone_number = models.CharField(
        "Numéro de téléphone",
        max_length=20,
        blank=True,
    )
    is_verified = models.BooleanField("Email vérifié", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
