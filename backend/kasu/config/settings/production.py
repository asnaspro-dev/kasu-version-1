"""
Settings pour l'environnement de production.
"""
from .base import *  # noqa: F401, F403

DEBUG = False

# CORS restrictif
CORS_ALLOW_ALL_ORIGINS = False
# Définir CORS_ALLOWED_ORIGINS dans l'environnement

# Sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
