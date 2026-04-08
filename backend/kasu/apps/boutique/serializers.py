"""
Serializers pour l'app boutique.
"""
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import BoutiqueProfile


class BoutiqueProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil boutique."""

    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = BoutiqueProfile
        fields = [
            "id",
            "user",
            "shop_name",
            "address",
            "city",
            "country",
            "latitude",
            "longitude",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BoutiqueProfileWriteSerializer(serializers.ModelSerializer):
    """Serializer pour création/mise à jour (sans user imbriqué)."""

    class Meta:
        model = BoutiqueProfile
        fields = [
            "shop_name",
            "address",
            "city",
            "country",
            "latitude",
            "longitude",
        ]
