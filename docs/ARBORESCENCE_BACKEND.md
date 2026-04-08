# Arborescence Backend KASU

```
kasuCursor/
├── docs/
│   ├── ARCHITECTURE_BACKEND.md   # Architecture détaillée
│   ├── ARBORESCENCE_BACKEND.md   # Ce fichier
│   └── PACKAGES_BACKEND.md       # Liste des packages
│
└── backend/
    ├── requirements.txt
    ├── .env.example
    │
    └── kasu/
        ├── manage.py
        ├── config/
        │   ├── __init__.py
        │   ├── settings/
        │   │   ├── __init__.py
        │   │   ├── base.py        # Settings communs
        │   │   ├── development.py # Dev
        │   │   ├── production.py  # Prod
        │   │   └── test.py        # Tests (SQLite)
        │   ├── urls.py
        │   ├── asgi.py
        │   └── wsgi.py
        │
        ├── apps/
        │   ├── accounts/          # User, JWT
        │   │   ├── models.py
        │   │   ├── serializers.py
        │   │   ├── admin.py
        │   │   └── urls.py
        │   ├── boutique/          # BoutiqueProfile
        │   ├── transitaire/       # TransitaireProfile
        │   ├── catalog/           # Category, Product
        │   ├── orders/            # Order, OrderItem
        │   ├── payments/          # Payment
        │   ├── escrow/            # EscrowTransaction
        │   ├── delivery/          # Delivery
        │   ├── notifications/     # Notification
        │   └── admin_site/        # SystemSetting, AuditLog
        │
        └── shared/                # Utilitaires partagés
```

## Rôle des apps

| App | Fichiers principaux | Rôle |
|-----|---------------------|------|
| accounts | models.py, serializers.py | User (CustomUser), JWT (email + password) |
| boutique | models.py, serializers.py | Profil boutique, adresse |
| transitaire | models.py, serializers.py | Profil transitaire, statut actif/archivé |
| catalog | models.py, serializers.py | Catégories, produits (MOQ, max_quantity) |
| orders | models.py, serializers.py | Commandes, lignes |
| payments | models.py, serializers.py | Paiements Mobile Money |
| escrow | models.py, serializers.py | Séquestre des fonds |
| delivery | models.py, serializers.py | Livraisons, validation |
| notifications | models.py, serializers.py | Notifications in-app |
| admin_site | models.py, serializers.py | Paramètres, audit |
