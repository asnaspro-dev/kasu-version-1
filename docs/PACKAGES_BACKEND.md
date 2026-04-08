# Packages Backend KASU

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Liste des packages

| Package | Version | Usage |
|---------|---------|-------|
| Django | >=5.0,<6.0 | Framework web |
| djangorestframework | >=3.14 | API REST |
| djangorestframework-simplejwt | >=5.3 | Authentification JWT |
| django-filter | >=23.0 | Filtrage des querysets |
| psycopg[binary] | >=3.1 | Driver PostgreSQL |
| drf-spectacular | >=0.27 | Documentation API OpenAPI |
| django-cors-headers | >=4.3 | CORS pour frontend |
| python-dotenv | >=1.0 | Variables d'environnement |

## Packages optionnels (prévus)

- celery : tâches asynchrones
- redis : broker Celery, cache
