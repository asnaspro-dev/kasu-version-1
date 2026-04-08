"""
Serializers pour l'app accounts.
Auth JWT avec email, inscription, profil utilisateur.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour lecture/écriture du User."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "role",
            "phone_number",
            "first_name",
            "last_name",
            "is_verified",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_verified"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour inscription (création de compte)."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "role",
            "phone_number",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})
        attrs.pop("password_confirm")
        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.username = validated_data["email"]  # Compatibilité Django
        user.save()
        return user


class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer léger pour affichage public (ex: dans une commande)."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT avec email au lieu de username.
    Le client envoie { "email": "...", "password": "..." }.
    Inclut les infos utilisateur dans la réponse.
    """
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        # Authentification par email
        from django.contrib.auth import authenticate
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,  # AUTH_USER_MODEL utilise email comme USERNAME_FIELD
            password=password,
        )
        if user is None:
            raise serializers.ValidationError("Identifiants invalides.")
        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }
