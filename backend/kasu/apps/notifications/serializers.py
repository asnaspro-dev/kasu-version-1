"""
Serializers pour l'app notifications.
"""
from rest_framework import serializers

from .models import Notification, NotificationType


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications."""

    notification_type = serializers.ChoiceField(
        choices=NotificationType.choices,
        read_only=True,
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "link",
            "is_read",
            "read_at",
            "created_at",
        ]
        read_only_fields = fields


class NotificationMarkReadSerializer(serializers.Serializer):
    """Serializer pour marquer une notification comme lue."""

    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="IDs des notifications à marquer. Vide = toutes.",
    )
