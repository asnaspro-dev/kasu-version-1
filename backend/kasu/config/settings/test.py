"""
Settings pour les tests.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# Base SQLite en mémoire pour tests rapides
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Password hashing plus rapide en tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
