# 🛒 Plateforme E-Commerce Multi-Vendeurs

Une plateforme e-commerce Django permettant aux vendeurs de gérer leurs boutiques et aux clients de commander des produits.

## 📋 Fonctionnalités

### Pour les Vendeurs
- 📊 Dashboard avec statistiques de ventes (graphiques interactifs)
- 📦 Gestion complète des produits (CRUD)
- 🗂️ Gestion des catégories
- 📸 Upload d'images pour les produits
- 🧾 Suivi des commandes en temps réel
- 📥 Export des ventes en CSV
- 🏪 Page boutique personnalisée

### Pour les Clients
- 🛍️ Navigation par catégories
- 🔍 Recherche de produits
- 🛒 Panier d'achat
- 💳 Processus de commande
- 📱 Dashboard avec historique des commandes
- 🏬 Consultation des différentes boutiques

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/Eren-73/Ecom.git
cd Ecom
```

2. **Créer et activer l'environnement virtuel**
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**
```bash
python manage.py migrate
```

5. **Créer un superutilisateur (Admin)**
```bash
python manage.py createsuperuser
```
Suivez les instructions pour créer votre compte admin.

6. **Créer des comptes de test** (Recommandé pour tester l'application)

**Créer un compte vendeur:**
- Allez sur http://127.0.0.1:8000/accounts/signup/vendor/
- Remplissez le formulaire (nom d'entreprise, description, etc.)
- Connectez-vous et ajoutez des produits depuis le dashboard

**Créer un compte client:**
- Allez sur http://127.0.0.1:8000/accounts/signup/customer/
- Remplissez le formulaire
- Vous pouvez maintenant parcourir et commander

**Ou créer des données via l'admin:**
- Allez sur http://127.0.0.1:8000/admin/
- Connectez-vous avec le superuser
- Créez des catégories, produits, profils vendeurs, etc.

7. **Créer les dossiers média (si nécessaire)**
```bash
# Windows
mkdir media\products media\vendors media\categories

# Linux/Mac
mkdir -p media/products media/vendors media/categories
```

8. **Lancer le serveur**
```bash
python manage.py runserver
```

9. **Accéder à l'application**
- Frontend: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 📁 Structure du Projet

```
Ecom/
├── accounts/           # Gestion des utilisateurs (vendeurs & clients)
├── products/           # Gestion des produits et catégories
├── orders/             # Gestion des commandes et paniers
├── templates/          # Templates HTML globaux
├── static/             # Fichiers statiques (CSS, JS, images)
├── media/              # Fichiers uploadés (images produits, etc.)
├── ecommerce_platform/ # Configuration Django principale
├── db.sqlite3          # Base de données SQLite
├── manage.py           # Script de gestion Django
└── requirements.txt    # Dépendances Python
```

## 👥 Types de Comptes

### Compte Vendeur
Pour créer un compte vendeur, allez sur:
- http://127.0.0.1:8000/accounts/signup/vendor/

Vous pourrez ensuite:
- Ajouter des produits
- Gérer vos catégories
- Voir vos statistiques de vente
- Suivre les commandes

### Compte Client
Pour créer un compte client, allez sur:
- http://127.0.0.1:8000/accounts/signup/customer/

Vous pourrez ensuite:
- Parcourir les produits
- Ajouter au panier
- Passer des commandes
- Suivre vos commandes

## 🔧 Configuration

### Variables d'environnement (optionnel)
Pour la production, créez un fichier `.env` avec:
```
SECRET_KEY=votre_secret_key_django
DEBUG=False
STRIPE_PUBLIC_KEY=votre_cle_publique_stripe
STRIPE_SECRET_KEY=votre_cle_secrete_stripe
```

### Base de données
Par défaut, le projet utilise SQLite. Pour PostgreSQL en production, modifiez `settings.py`.

## 📊 Technologies Utilisées

- **Backend**: Django 5.2.7
- **Base de données**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Graphiques**: Chart.js
- **Images**: Pillow
- **Paiement**: Stripe (intégration prévue)

## ⚠️ Notes Importantes

1. **STRIPE_SECRET_KEY**: Configurez vos clés Stripe dans `settings.py` pour le paiement
2. **DEBUG**: Mettez `DEBUG = False` en production
3. **ALLOWED_HOSTS**: Ajoutez votre domaine en production
4. **Fichiers média**: Assurez-vous que les dossiers `media/` ont les bonnes permissions

## 🐛 Problèmes Connus

- **Warning template tag**: Le fichier `custom_filters.py` est dupliqué dans `accounts` et `orders`. C'est normal.
- **Stripe**: Les paiements ne fonctionneront pas sans configuration Stripe valide.

## 📝 Commandes Utiles

```bash
# Créer de nouvelles migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Collecter les fichiers statiques (pour production)
python manage.py collectstatic

# Lancer les tests
python manage.py test
```

## 🆘 Support & Dépannage

### Problème: "No such table" ou "no such column"
```bash
python manage.py migrate
```

### Problème: "STATICFILES_DIRS does not exist"
```bash
# Windows
mkdir static

# Linux/Mac
mkdir static
```

### Problème: Import errors
Vérifiez que l'environnement virtuel est activé et les dépendances installées:
```bash
pip install -r requirements.txt
```

## 👨‍💻 Auteur

Développé par **Eren73**

## 📄 Licence

Ce projet est sous licence libre pour usage éducatif.

---

**Bon test! 🚀** Si vous rencontrez des problèmes, vérifiez que:
1. L'environnement virtuel est activé
2. Toutes les dépendances sont installées
3. Les migrations sont appliquées
4. Le serveur tourne sur le bon port