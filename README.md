# 🛒 Plateforme E-Commerce Multi-Vendeurs

Une plateforme e-commerce moderne développée avec Django, permettant aux vendeurs de gérer leurs boutiques et aux clients de commander des produits en toute simplicité.

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple)

---

## ✨ Fonctionnalités Principales

### 👨‍💼 Pour les Vendeurs
- 📊 **Dashboard interactif** avec statistiques de ventes et graphiques (Chart.js)
- 📦 **Gestion complète des produits** (création, modification, suppression)
- 🗂️ **Gestion des catégories**
- 📸 **Upload d'images** pour les produits
- 🧾 **Suivi des commandes** en temps réel avec changement de statut
- 📥 **Export des données** en CSV
- 🏪 **Page boutique personnalisée** pour chaque vendeur
- 🎨 **Interface moderne** avec design gradient violet

### 🛍️ Pour les Clients
- 🏠 **Page d'accueil moderne** avec navigation intuitive
- 🔍 **Recherche et filtrage** par catégories
- 🛒 **Panier d'achat dynamique**
- 💳 **Processus de commande** fluide et sécurisé
- 📱 **Dashboard personnel** avec historique des commandes
- 🏬 **Consultation des boutiques** des différents vendeurs
- ✨ **Design responsive** adapté à tous les écrans

---

## 🚀 Installation et Configuration

### Prérequis
- **Python 3.10** ou supérieur
- **pip** (gestionnaire de paquets Python)
- **Git**

### Étapes d'installation

#### 1. Cloner le repository
```bash
git clone https://github.com/Eren-73/Ecom.git
cd Ecom
```

#### 2. Créer et activer l'environnement virtuel

**Windows (PowerShell) :**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
python -m venv env
.\env\Scripts\activate.bat
```

**Linux/macOS :**
```bash
python3 -m venv env
source env/bin/activate
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Configuration de la base de données
```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

#### 5. Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
```
Suivez les instructions pour définir :
- Nom d'utilisateur
- Email
- Mot de passe

#### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```

L'application sera accessible sur **http://127.0.0.1:8000/**

---

## 📖 Guide d'Utilisation

### 🔐 Première Connexion

#### Accès Admin (Panel d'administration)
- URL : `http://127.0.0.1:8000/admin/`
- Utilisez les identifiants du superutilisateur créé

#### Création de Comptes

**Pour devenir Vendeur :**
1. Allez sur la page d'accueil
2. Cliquez sur **"Inscription Vendeur"**
3. Remplissez le formulaire :
   - Nom d'utilisateur
   - Email
   - Mot de passe (confirmation requise)
   - Nom de la boutique
   - Description
   - Téléphone
   - Adresse
   - Ville
   - Logo (optionnel)
4. Soumettez le formulaire
5. Vous serez automatiquement connecté et redirigé vers votre **Dashboard Vendeur**

**Pour devenir Client :**
1. Allez sur la page d'accueil
2. Cliquez sur **"Inscription Client"**
3. Remplissez le formulaire :
   - Nom d'utilisateur
   - Email
   - Mot de passe (confirmation requise)
   - Téléphone (optionnel)
   - Adresse (optionnel)
   - Ville (optionnel)
4. Soumettez le formulaire
5. Vous serez automatiquement connecté et redirigé vers votre **Dashboard Client**

---

### 👨‍💼 Guide Vendeur

#### Dashboard Vendeur
Après connexion, vous accédez à votre dashboard qui affiche :
- **Statistiques de ventes** avec graphiques interactifs
- **Ventes par mois** (graphique linéaire)
- **Produits les plus vendus** (graphique en barres)
- **Liste de vos produits**
- **Commandes reçues**

#### Gestion des Produits

**Ajouter un produit :**
1. Dans le dashboard, cliquez sur **"➕ Ajouter un produit"**
2. Remplissez les informations :
   - Nom du produit
   - Description
   - Prix
   - Stock disponible
   - Catégorie
   - Image
3. Cliquez sur **"Créer"**

**Modifier un produit :**
1. Dans la liste des produits, cliquez sur **"✏️ Modifier"**
2. Modifiez les informations souhaitées
3. Cliquez sur **"Mettre à jour"**

**Supprimer un produit :**
1. Cliquez sur **"🗑️ Supprimer"**
2. Confirmez la suppression

#### Gestion des Catégories
1. Cliquez sur **"➕ Ajouter une catégorie"**
2. Entrez le nom de la catégorie
3. Sauvegardez

#### Gestion des Commandes
- Visualisez toutes les commandes contenant vos produits
- **Changez le statut** des commandes :
  - En attente
  - Confirmée
  - En traitement
  - Expédiée
  - Livrée
- Filtrez les commandes par statut

#### Export des Données
- Cliquez sur **"📥 Télécharger CSV"** pour exporter la liste de vos produits

---

### 🛍️ Guide Client

#### Dashboard Client
Après connexion, vous accédez à votre dashboard qui affiche :
- **Statistiques personnelles** :
  - Nombre total de commandes
  - Commandes en attente
  - Commandes livrées
- **Liste de vos commandes récentes**

#### Navigation et Recherche
- Parcourez les **catégories** sur la page d'accueil
- Utilisez la **barre de recherche** pour trouver des produits
- Cliquez sur un produit pour voir ses **détails**

#### Passer une Commande

**1. Ajouter au panier :**
- Sur la page d'un produit, cliquez sur **"🛒 Ajouter au panier"**
- Choisissez la quantité souhaitée

**2. Consulter le panier :**
- Cliquez sur **"Panier"** dans la navigation
- Vous verrez tous les produits ajoutés
- Modifiez les quantités si nécessaire
- Cliquez sur **"Procéder au paiement"**

**3. Finaliser la commande :**
- Remplissez vos informations de livraison
- Vérifiez le récapitulatif
- Cliquez sur **"Confirmer la commande"**

#### Suivi des Commandes
- Accédez à **"Historique"** pour voir toutes vos commandes
- Cliquez sur **"Voir les détails"** pour voir le détail d'une commande
- Suivez le **statut** de vos commandes en temps réel

#### Découvrir les Boutiques
- Consultez la **liste des boutiques** disponibles
- Visitez la page d'une boutique pour voir ses produits

---

## 📁 Structure du Projet

```
Ecom/
├── accounts/                    # Gestion des utilisateurs
│   ├── models.py               # VendorProfile, CustomerProfile
│   ├── views.py                # Dashboards, signup, login
│   ├── forms.py                # Formulaires d'inscription
│   └── templates/accounts/     # Templates vendeur/client
├── products/                    # Gestion des produits
│   ├── models.py               # Product, Category
│   ├── views.py                # CRUD produits/catégories
│   └── templates/products/     # Templates produits
├── orders/                      # Gestion des commandes
│   ├── models.py               # Cart, Order, OrderItem
│   ├── views.py                # Panier, checkout, historique
│   └── templates/orders/       # Templates commandes
├── ecommerce_platform/          # Configuration Django
│   ├── settings.py             # Configuration générale
│   ├── urls.py                 # Routes principales
│   └── views.py                # Page d'accueil
├── templates/                   # Templates globaux
├── media/                       # Images uploadées
├── static/                      # Fichiers statiques (CSS, JS)
├── db.sqlite3                   # Base de données SQLite
├── manage.py                    # Script Django
└── requirements.txt             # Dépendances Python
```

---

## �️ Technologies Utilisées

### Backend
- **Django 5.2.7** - Framework web Python
- **SQLite** - Base de données (développement)
- **Pillow** - Traitement d'images

### Frontend
- **Bootstrap 5.3.2** - Framework CSS
- **Font Awesome 6.4.0** - Icônes
- **Chart.js** - Graphiques interactifs
- **Vanilla JavaScript** - Interactivité

### Design
- **Gradient violet moderne** (#667eea → #764ba2)
- **Responsive design**
- **Animations et transitions fluides**

---

## 🔧 Configuration Avancée

### Variables d'Environnement
Pour la production, configurez les variables suivantes :
- `SECRET_KEY` - Clé secrète Django
- `DEBUG` - Mode debug (False en production)
- `ALLOWED_HOSTS` - Domaines autorisés
- `DATABASE_URL` - URL de la base de données

### Collecte des fichiers statiques
```bash
python manage.py collectstatic
```

### Déploiement
Le projet est prêt pour le déploiement sur :
- **Heroku**
- **PythonAnywhere**
- **DigitalOcean**
- **AWS**

---

## � Dépannage

### Problème : Module not found
```bash
pip install -r requirements.txt
```

### Problème : Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problème : Port déjà utilisé
```bash
# Utiliser un autre port
python manage.py runserver 8001
```

### Problème : Images ne s'affichent pas
Vérifiez que `MEDIA_URL` et `MEDIA_ROOT` sont configurés dans `settings.py`

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```
3. **Commit** vos changements
   ```bash
   git commit -m "Ajout d'une nouvelle fonctionnalité"
   ```
4. **Push** vers la branche
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```
5. Ouvrez une **Pull Request**

---

## � License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteur

**Eren-73**
- GitHub: [@Eren-73](https://github.com/Eren-73)

---

## � Support

Pour toute question ou problème :
- Ouvrez une **issue** sur GitHub
- Contactez-moi via mon profil GitHub

---

## 🚀 Roadmap

### Fonctionnalités à venir
- [ ] Système de paiement en ligne (Stripe/PayPal)
- [ ] Système de notation et avis clients
- [ ] Chat en temps réel vendeur-client
- [ ] Notifications par email
- [ ] Système de wishlist
- [ ] Codes promo et réductions
- [ ] Multi-langues (i18n)
- [ ] API REST avec Django REST Framework
- [ ] Application mobile (React Native)

---

## 🙏 Remerciements

Merci d'utiliser cette plateforme e-commerce ! N'hésitez pas à ⭐ le projet si vous le trouvez utile.

---

**Développé avec ❤️ et Django**