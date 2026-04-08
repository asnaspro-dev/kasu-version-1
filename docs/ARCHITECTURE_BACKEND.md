# Architecture Backend KASU

## 1. Vue d'ensemble

KASU est une plateforme B2B d'approvisionnement connectant boutiques et transitaires. L'architecture backend repose sur **Django 5+**, **Django REST Framework** et **PostgreSQL**.

### Principes architecturaux
- **Modularité** : une app Django par domaine fonctionnel
- **Séparation des responsabilités** : modèles, serializers, views, services métier distincts
- **Extensibilité** : préparation pour Celery, Redis, notifications
- **Sécurité** : JWT, permissions par rôle, validation stricte

---

## 2. Arborescence des apps Django

```
kasu/
├── config/                 # Configuration projet (settings, urls racine)
├── apps/
│   ├── accounts/           # Utilisateurs, authentification, rôles
│   ├── boutique/           # Profil boutique, adresses
│   ├── transitaire/        # Profil transitaire
│   ├── catalog/            # Catégories, produits
│   ├── orders/             # Commandes, OrderItem
│   ├── payments/           # Paiements, Mobile Money
│   ├── escrow/             # Séquestre
│   ├── delivery/           # Livraisons
│   ├── notifications/      # Notifications
│   └── admin_site/         # Admin, paramètres système, audit
└── shared/                 # Utilitaires partagés
```

**Décision** : séparer `escrow` et `payments` car ce sont des concepts métier distincts (collecte vs détention des fonds).

---

## 3. Architecture des couches

```
┌─────────────────────────────────────────────────────────┐
│                    API REST (DRF)                        │
│  ViewSets → Permissions → Serializers                    │
├─────────────────────────────────────────────────────────┤
│                  Services métier                         │
│  OrderService, PaymentService, EscrowService, etc.       │
├─────────────────────────────────────────────────────────┤
│                   Modèles Django                         │
│  User, Product, Order, Payment, EscrowTransaction...     │
├─────────────────────────────────────────────────────────┤
│                   PostgreSQL                             │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Modèles et responsabilités

| App | Modèles | Responsabilité |
|-----|---------|----------------|
| accounts | User (CustomUser) | Authentification, rôles (boutique, transitaire, admin) |
| boutique | BoutiqueProfile | Profil boutique, infos livraison |
| transitaire | TransitaireProfile | Profil transitaire, statut (actif/archivé) |
| catalog | Category, Product | Catalogue produits avec MOQ, max_quantity |
| orders | Order, OrderItem | Commandes, ligne de commande |
| payments | Payment | Paiements Mobile Money |
| escrow | EscrowTransaction | Séquestre, commission, libération |
| delivery | Delivery | Livraison, validation boutique |
| notifications | Notification | Notifications in-app |
| admin_site | SystemSetting, AuditLog | Config commission, traçabilité |

---

## 5. Flux métier principaux

### Commande
1. Boutique choisit produit(s) → création Order + OrderItem(s)
2. Validation quantités : MOQ ≤ quantité ≤ max_quantity
3. Status Order = PENDING_PAYMENT

### Paiement
1. Boutique paie via Mobile Money
2. Payment créé, status = COMPLETED
3. EscrowTransaction créée, release_status = LOCKED
4. Order status = PAID

### Livraison
1. Transitaire livre → Delivery.started_at
2. Boutique valide → Delivery.validated_by_boutique_at
3. Escrow release_status = RELEASED
4. Transitaire reçoit net_amount (après commission)

---

## 6. Authentification et permissions

- **JWT** : simplejwt (access + refresh tokens)
- **Custom User** : email comme identifiant principal
- **Permissions** : IsBoutique, IsTransitaire, IsAdmin
- **Object-level** : IsOrderOwner, IsProductTransitaire, etc.

---

## 7. Paramètres configurables

- `SystemSetting` : commission_rate (Decimal, global)
- Modifiable par Admin uniquement
- Utilisé à la création de chaque commande pour fixer la commission

---

## 8. Évolutivité prévue

- **Celery** : tâches asynchrones (emails, notifications, webhooks)
- **Redis** : cache, broker Celery
- **Signals** : création Order, validation Delivery, etc.
