# Script pour créer des comptes de test avec mots de passe connus
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_platform.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CustomerProfile, VendorProfile

print("=" * 60)
print("🔧 CRÉATION DE COMPTES DE TEST")
print("=" * 60)

# Mot de passe pour tous les comptes
PASSWORD = "test1234"

# ============== CRÉER UN CLIENT DE TEST ==============
print("\n👤 Création d'un compte CLIENT...")
try:
    # Supprimer si existe déjà
    if User.objects.filter(username='client_test').exists():
        User.objects.get(username='client_test').delete()
        print("  ✓ Ancien compte supprimé")
    
    # Créer le user
    client_user = User.objects.create_user(
        username='client_test',
        email='client@test.com',
        password=PASSWORD,
        first_name='Jean',
        last_name='Dupont'
    )
    
    # Créer le profil client
    customer_profile = CustomerProfile.objects.create(
        user=client_user,
        phone='0612345678',
        address='123 Rue de Paris',
        city='Paris'
    )
    
    print("  ✅ CLIENT créé avec succès!")
    print(f"     Username: client_test")
    print(f"     Email: client@test.com")
    print(f"     Password: {PASSWORD}")
    
except Exception as e:
    print(f"  ❌ Erreur: {e}")

# ============== CRÉER UN VENDEUR DE TEST ==============
print("\n🏪 Création d'un compte VENDEUR...")
try:
    # Supprimer si existe déjà
    if User.objects.filter(username='vendeur_test').exists():
        User.objects.get(username='vendeur_test').delete()
        print("  ✓ Ancien compte supprimé")
    
    # Créer le user
    vendor_user = User.objects.create_user(
        username='vendeur_test',
        email='vendeur@test.com',
        password=PASSWORD,
        first_name='Marie',
        last_name='Martin'
    )
    
    # Créer le profil vendeur
    vendor_profile = VendorProfile.objects.create(
        user=vendor_user,
        business_name='Ma Super Boutique',
        description='Boutique de test avec des produits variés',
        phone='0698765432',
        address='456 Avenue des Champs',
        city='Lyon'
    )
    
    print("  ✅ VENDEUR créé avec succès!")
    print(f"     Username: vendeur_test")
    print(f"     Email: vendeur@test.com")
    print(f"     Password: {PASSWORD}")
    print(f"     Boutique: {vendor_profile.business_name}")
    
except Exception as e:
    print(f"  ❌ Erreur: {e}")

# ============== RÉINITIALISER DES COMPTES EXISTANTS ==============
print("\n🔄 Réinitialisation de comptes existants...")

# Réinitialiser alice45857 (client)
try:
    user = User.objects.get(username='alice45857')
    user.set_password(PASSWORD)
    user.save()
    print(f"  ✅ alice45857 - Password: {PASSWORD}")
except:
    print("  ⚠️  alice45857 non trouvé")

# Réinitialiser thibaut83100 (vendeur)
try:
    user = User.objects.get(username='thibaut83100')
    user.set_password(PASSWORD)
    user.save()
    print(f"  ✅ thibaut83100 (Denis SA) - Password: {PASSWORD}")
except:
    print("  ⚠️  thibaut83100 non trouvé")

print("\n" + "=" * 60)
print("✅ TERMINÉ!")
print("=" * 60)
print("\n📝 COMPTES DISPONIBLES POUR TEST:")
print("\n🛍️ CLIENTS:")
print("   • client_test / client@test.com")
print("   • alice45857 / marcel24@example.com")
print("\n🏪 VENDEURS:")
print("   • vendeur_test / vendeur@test.com (Ma Super Boutique)")
print("   • thibaut83100 / ngay@example.net (Denis SA)")
print(f"\n🔐 Mot de passe pour tous: {PASSWORD}")
print("=" * 60)
