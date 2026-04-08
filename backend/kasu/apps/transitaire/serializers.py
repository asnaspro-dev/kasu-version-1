"""
Serializers pour l'app transitaire.
"""
from rest_framework import serializers

from apps.accounts.serializers import UserPublicSerializer

from .models import TransitaireProfile, TransitaireStatus


class TransitaireProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil transitaire (lecture)."""

    user = UserPublicSerializer(read_only=True)
    status = serializers.ChoiceField(choices=TransitaireStatus.choices, read_only=True)

    class Meta:
        model = TransitaireProfile
        fields = [
            "id",
            "user",
            "company_name",
            "status",
            "archived_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "archived_at", "created_at", "updated_at"]


class TransitaireProfileWriteSerializer(serializers.ModelSerializer):
    """Serializer pour création/mise à jour du profil transitaire."""

    class Meta:
        model = TransitaireProfile
        fields = ["company_name"]


class TransitairePublicSerializer(serializers.Serializer):
    """
    Serializer pour afficher un transitaire (User) avec company_name.
    À utiliser avec User (transitaire) : order.transitaire, product.transitaire.
    """

    id = serializers.IntegerField()
    email = serializers.EmailField()
    company_name = serializers.SerializerMethodField()

    def get_company_name(self, obj):
        try:
            return obj.transitaire_profile.company_name
        except TransitaireProfile.DoesNotExist:
            return ""
