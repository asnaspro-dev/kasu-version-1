"""
Modèles pour l'app admin_site.
Paramètres système et audit.
"""
from decimal import Decimal

from django.conf import settings
from django.db import models


class SystemSetting(models.Model):
    """
    Paramètre système configuré par l'admin.
    Ex: commission_rate (taux global de commission).
    """

    key = models.CharField("Clé", max_length=100, unique=True)
    value = models.TextField("Valeur")
    value_type = models.CharField(
        "Type",
        max_length=20,
        choices=[
            ("str", "Chaîne"),
            ("int", "Entier"),
            ("decimal", "Décimal"),
            ("bool", "Booléen"),
        ],
        default="str",
    )
    description = models.CharField(
        "Description",
        max_length=255,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admin_site_systemsetting"
        verbose_name = "Paramètre système"
        verbose_name_plural = "Paramètres système"

    def __str__(self):
        return f"{self.key} = {self.value}"

    def get_value(self):
        """Retourne la valeur typée."""
        if self.value_type == "int":
            return int(self.value)
        if self.value_type == "decimal":
            return Decimal(self.value)
        if self.value_type == "bool":
            return self.value.lower() in ("true", "1", "yes")
        return self.value


class AuditLog(models.Model):
    """
    Journal d'audit pour traçabilité.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField("Action", max_length=100)
    model_name = models.CharField("Modèle", max_length=100, blank=True)
    object_id = models.CharField("ID objet", max_length=100, blank=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_site_auditlog"
        verbose_name = "Entrée d'audit"
        verbose_name_plural = "Journal d'audit"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.created_at}"
