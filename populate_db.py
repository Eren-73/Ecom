# d:\Projets\Ecom\populate_db.py
# Script pour populer la base de données avec des données de test réalistes
# Usage: python populate_db.py
# RELEVANT FILES: manage.py, accounts/models.py, products/models.py, orders/models.py

import os
import django
import random
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_platform.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import VendorProfile, CustomerProfile
from products.models import Category, Product
from orders.models import Order, OrderItem, Cart, CartItem
from faker import Faker

# Initialiser Faker en français
fake = Faker('fr_FR')

def clear_database():
    """Supprimer toutes les données existantes (sauf superusers)"""
    print("🗑️  Nettoyage de la base de données...")
    
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    VendorProfile.objects.all().delete()
    CustomerProfile.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    print("✅ Base de données nettoyée!")

def create_categories():
    """Créer des catégories de produits"""
    print("\n📂 Création des catégories...")
    
    categories_data = [
        ("Électronique", "Smartphones, ordinateurs, accessoires high-tech"),
        ("Mode", "Vêtements, chaussures, accessoires de mode"),
        ("Maison & Jardin", "Meubles, décoration, outils de jardinage"),
        ("Sports & Loisirs", "Équipements sportifs, jeux, loisirs créatifs"),
        ("Beauté & Santé", "Cosmétiques, produits de soin, bien-être"),
        ("Alimentation", "Produits alimentaires, boissons, épicerie fine"),
        ("Livres & Médias", "Livres, films, musique, jeux vidéo"),
        ("Jouets & Enfants", "Jouets, vêtements enfants, articles de puériculture"),
    ]
    
    categories = []
    for name, description in categories_data:
        category = Category.objects.create(
            name=name,
            description=description
        )
        categories.append(category)
        print(f"  ✓ {name}")
    
    return categories

def create_vendors(count=5):
    """Créer des comptes vendeurs"""
    print(f"\n🏪 Création de {count} vendeurs...")
    
    vendors = []
    for i in range(count):
        # Créer l'utilisateur
        username = fake.user_name() + str(random.randint(100, 999))
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        
        # Créer le profil vendeur
        vendor = VendorProfile.objects.create(
            user=user,
            business_name=fake.company(),
            description=fake.text(max_nb_chars=200),
            phone=fake.phone_number(),
            address=fake.street_address(),
            city=fake.city(),
            is_verified=True
        )
        vendors.append(vendor)
        print(f"  ✓ {vendor.business_name} (@{username})")
    
    return vendors

def create_customers(count=10):
    """Créer des comptes clients"""
    print(f"\n👥 Création de {count} clients...")
    
    customers = []
    for i in range(count):
        # Créer l'utilisateur
        username = fake.user_name() + str(random.randint(100, 999))
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        
        # Créer le profil client
        customer = CustomerProfile.objects.create(
            user=user,
            phone=fake.phone_number(),
            address=fake.street_address(),
            city=fake.city()
        )
        customers.append(customer)
        print(f"  ✓ {user.get_full_name()} (@{username})")
    
    return customers

def create_products(vendors, categories, count_per_vendor=10):
    """Créer des produits pour chaque vendeur"""
    print(f"\n📦 Création de produits ({count_per_vendor} par vendeur)...")
    
    products = []
    product_names = [
        "Smartphone", "Ordinateur portable", "Casque audio", "Montre connectée",
        "T-shirt", "Jean", "Baskets", "Sac à main", "Lunettes de soleil",
        "Table", "Chaise", "Lampe", "Tapis", "Coussin",
        "Ballon de football", "Raquette de tennis", "Vélo", "Tapis de yoga",
        "Crème hydratante", "Parfum", "Shampooing", "Maquillage",
        "Livre", "DVD", "Jeu vidéo", "Console", "Manga",
        "Jouet en bois", "Puzzle", "Peluche", "LEGO"
    ]
    
    for vendor in vendors:
        for i in range(count_per_vendor):
            category = random.choice(categories)
            base_name = random.choice(product_names)
            
            product = Product.objects.create(
                vendor=vendor,
                name=f"{base_name} {fake.word().capitalize()}",
                description=fake.text(max_nb_chars=300),
                price=Decimal(str(round(random.uniform(10, 500), 2))),
                category=category,
                stock_quantity=random.randint(0, 100),
                is_active=random.choice([True, True, True, False]),  # 75% actifs
                tags=", ".join(fake.words(nb=random.randint(2, 5)))
            )
            products.append(product)
        
        print(f"  ✓ {count_per_vendor} produits pour {vendor.business_name}")
    
    return products

def create_orders(customers, products, count=20):
    """Créer des commandes"""
    print(f"\n🛒 Création de {count} commandes...")
    
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    for i in range(count):
        customer = random.choice(customers)
        
        # Créer la commande
        order = Order.objects.create(
            customer=customer.user,
            shipping_address=fake.address(),
            status=random.choice(statuses),
            total_amount=Decimal('0')
        )
        
        # Ajouter des items à la commande
        num_items = random.randint(1, 5)
        total = Decimal('0')
        
        selected_products = random.sample(products, min(num_items, len(products)))
        for product in selected_products:
            quantity = random.randint(1, 3)
            price = product.price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            
            total += price * quantity
        
        # Mettre à jour le montant total
        order.total_amount = total
        order.save()
        
        print(f"  ✓ Commande #{order.order_number} - {customer.user.username} - {total}€")

def create_carts(customers, products):
    """Créer des paniers pour certains clients"""
    print(f"\n🛍️  Création de paniers actifs...")
    
    # Créer des paniers pour 50% des clients
    for customer in random.sample(customers, len(customers) // 2):
        cart = Cart.objects.create(user=customer.user)
        
        # Ajouter des produits au panier
        num_items = random.randint(1, 4)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        for product in selected_products:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=random.randint(1, 3)
            )
        
        print(f"  ✓ Panier pour {customer.user.username} ({num_items} produits)")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 POPULATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    # Demander confirmation
    response = input("\n⚠️  Voulez-vous EFFACER toutes les données existantes ? (oui/non): ")
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        clear_database()
    
    # Créer les données
    categories = create_categories()
    vendors = create_vendors(count=5)
    customers = create_customers(count=10)
    products = create_products(vendors, categories, count_per_vendor=10)
    create_orders(customers, products, count=20)
    create_carts(customers, products)
    
    # Résumé
    print("\n" + "=" * 60)
    print("✅ POPULATION TERMINÉE!")
    print("=" * 60)
    print(f"📊 Résumé:")
    print(f"  • Catégories: {Category.objects.count()}")
    print(f"  • Vendeurs: {VendorProfile.objects.count()}")
    print(f"  • Clients: {CustomerProfile.objects.count()}")
    print(f"  • Produits: {Product.objects.count()}")
    print(f"  • Commandes: {Order.objects.count()}")
    print(f"  • Paniers actifs: {Cart.objects.count()}")
    print("\n📝 Identifiants de test:")
    print("  Username: n'importe quel username créé")
    print("  Password: password123")
    print(f"\n🌐 Lancer le serveur: python manage.py runserver")
    print("=" * 60)

if __name__ == '__main__':
    main()
