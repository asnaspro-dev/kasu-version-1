"""
Serializers pour l'app admin_site.
Paramètres système et audit.
"""
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import AuditLog, SystemSetting


class SystemSettingSerializer(serializers.ModelSerializer):
    """Serializer pour les paramètres système (admin)."""

    class Meta:
        model = SystemSetting
        fields = [
            "id",
            "key",
            "value",
            "value_type",
            "description",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class SystemSettingWriteSerializer(serializers.ModelSerializer):
    """Serializer pour mise à jour des paramètres."""

    class Meta:
        model = SystemSetting
        fields = ["key", "value", "value_type", "description"]


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer pour le journal d'audit (lecture seule)."""

    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "action",
            "model_name",
            "object_id",
            "details",
            "ip_address",
            "created_at",
        ]
        read_only_fields = fields
