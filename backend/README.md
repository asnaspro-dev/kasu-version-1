# KASU Backend

Backend Django pour la plateforme KASU (approvisionnement B2B).

## Prérequis

- Python 3.10+
- PostgreSQL (pour dev/prod)

## Installation

```bash
cd backend
pip install -r requirements.txt
```

Copier `.env.example` vers `.env` et adapter les variables.

## Configuration

- **Dev** : `DJANGO_SETTINGS_MODULE=config.settings.development`
- **Test** : `config.settings.test` (SQLite en mémoire)
- **Prod** : `config.settings.production`

## Commandes

```bash
cd kasu

# Vérification
python manage.py check

# Migrations (PostgreSQL)
python manage.py makemigrations
python manage.py migrate

# Migrations (SQLite pour tests)
python manage.py makemigrations --settings=config.settings.test
python manage.py migrate --settings=config.settings.test

# Serveur
python manage.py runserver
```

## API

- `/api/docs/` : Swagger UI
- `/api/schema/` : Schéma OpenAPI
- `/api/auth/token/` : Obtenir un JWT (POST email, password)
- `/api/auth/token/refresh/` : Rafraîchir le token
