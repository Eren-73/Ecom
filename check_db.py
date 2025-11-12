# Script pour vérifier les données dans la base de données
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_platform.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CustomerProfile, VendorProfile
from products.models import Product, Category
from orders.models import Order

print("=" * 60)
print("📊 DONNÉES DANS LA BASE DE DONNÉES")
print("=" * 60)

# Utilisateurs
print("\n👤 UTILISATEURS:")
users = User.objects.all()
for user in users:
    user_type = "Admin" if user.is_superuser else "User"
    print(f"  - {user.username} ({user.email}) - {user_type}")

# Clients
print("\n🛍️ CLIENTS:")
customers = CustomerProfile.objects.all()
if customers:
    for customer in customers:
        print(f"  - {customer.user.username}")
        print(f"    Email: {customer.user.email}")
        print()
else:
    print("  Aucun client enregistré")

# Vendeurs
print("\n🏪 VENDEURS:")
vendors = VendorProfile.objects.all()
if vendors:
    for vendor in vendors:
        print(f"  - {vendor.user.username}")
        print(f"    Email: {vendor.user.email}")
        print(f"    Boutique: {vendor.business_name}")
        print(f"    Adresse: {vendor.address}")
        print()
else:
    print("  Aucun vendeur enregistré")

# Catégories
print("\n📁 CATÉGORIES:")
categories = Category.objects.all()
if categories:
    for cat in categories:
        product_count = cat.products.count()
        print(f"  - {cat.name} ({product_count} produits)")
else:
    print("  Aucune catégorie")

# Produits
print("\n📦 PRODUITS:")
products = Product.objects.all()[:10]  # Limiter à 10 pour la lisibilité
if products:
    for product in products:
        vendor_name = product.vendor.business_name
        print(f"  - {product.name}")
        print(f"    Prix: {product.price}€")
        print(f"    Vendeur: {vendor_name}")
        print(f"    Catégorie: {product.category.name if product.category else 'N/A'}")
        print()
    total_products = Product.objects.count()
    if total_products > 10:
        print(f"  ... et {total_products - 10} autres produits")
else:
    print("  Aucun produit")

# Commandes
print("\n📋 COMMANDES:")
orders = Order.objects.all()
if orders:
    for order in orders:
        print(f"  - Commande #{order.id}")
        print(f"    Client: {order.customer.username}")
        print(f"    Montant: {order.total_amount}€")
        print(f"    Statut: {order.status}")
        print(f"    Date: {order.created_at.strftime('%d/%m/%Y %H:%M')}")
        print()
else:
    print("  Aucune commande")

print("=" * 60)
print(f"\n📊 RÉSUMÉ:")
print(f"  Total utilisateurs: {users.count()}")
print(f"  Total clients: {customers.count()}")
print(f"  Total vendeurs: {vendors.count()}")
print(f"  Total catégories: {categories.count()}")
print(f"  Total produits: {products.count()}")
print(f"  Total commandes: {orders.count()}")
print("=" * 60)
