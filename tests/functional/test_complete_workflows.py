"""
Tests fonctionnels - Scénarios métier complets (P1)
Workflows de bout en bout
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import VendorProfile
from products.models import Product, Category
from orders.models import Cart, Order


class TestWorkflowClientComplet(TestCase):
    """Workflow complet : Parcours client de bout en bout"""

    def setUp(self):
        self.client = Client()

    def test_parcours_client_complet(self):
        """Workflow complet : Inscription client → Navigation → Achat → Commande"""
        # Étape 1 : Inscription client
        data_inscription = {
            "username": "client_test",
            "email": "client@test.com",
            "password1": "Test1234!",
            "password2": "Test1234!",
            "phone": "0612345678",
            "address": "123 Rue Test",
            "city": "Paris",
        }
        response = self.client.post(
            reverse("customer_signup"), data_inscription
        )
        self.assertEqual(response.status_code, 302)

        client = User.objects.get(username="client_test")
        self.assertTrue(hasattr(client, "customer_profile"))

        # Étape 2 : Créer un vendeur et des produits
        vendeur_user = User.objects.create_user(
            username="vendeur", password="test"
        )
        vendeur = VendorProfile.objects.create(
            user=vendeur_user,
            business_name="Boutique Test",
            description="Description",
            phone="0612345678",
            address="123 Rue",
            city="Paris",
        )
        categorie = Category.objects.create(name="Électronique")
        produit1 = Product.objects.create(
            vendor=vendeur,
            name="Produit 1",
            description="Description",
            price=10.00,
            category=categorie,
            stock_quantity=10,
        )
        produit2 = Product.objects.create(
            vendor=vendeur,
            name="Produit 2",
            description="Description",
            price=20.00,
            category=categorie,
            stock_quantity=5,
        )

        # Étape 3 : Ajout au panier
        self.client.post(
            reverse("add_to_cart", kwargs={"product_id": produit1.pk}),
            {"quantity": 2},
        )
        self.client.post(
            reverse("add_to_cart", kwargs={"product_id": produit2.pk}),
            {"quantity": 1},
        )

        # Vérifier le panier
        panier = Cart.objects.get(user=client)
        self.assertEqual(panier.items.count(), 2)
        self.assertEqual(float(panier.total_amount), 40.00)

        # Étape 4 : Checkout
        data_checkout = {
            "shipping_address": "123 Rue Test",
            "shipping_city": "Paris",
            "shipping_phone": "0612345678",
        }
        response = self.client.post(reverse("checkout"), data_checkout)
        self.assertEqual(response.status_code, 302)

        # Vérifier la commande créée
        commande = Order.objects.get(customer=client)
        self.assertEqual(commande.status, "confirmed")
        self.assertEqual(float(commande.total_amount), 40.00)
        self.assertEqual(commande.items.count(), 2)
        self.assertEqual(panier.items.count(), 0)


class TestWorkflowVendeurComplet(TestCase):
    """Workflow complet : Parcours vendeur de bout en bout"""

    def setUp(self):
        self.client = Client()

    def test_parcours_vendeur_complet(self):
        """Workflow complet : Inscription vendeur → Création produit → Vente"""
        # Étape 1 : Inscription vendeur
        data_inscription = {
            "username": "vendeur_test",
            "email": "vendeur@test.com",
            "password1": "Test1234!",
            "password2": "Test1234!",
            "business_name": "Ma Boutique",
            "description": "Description boutique",
            "phone": "0612345678",
            "address": "123 Rue Test",
            "city": "Paris",
        }
        response = self.client.post(
            reverse("vendor_signup"), data_inscription
        )
        self.assertEqual(response.status_code, 302)

        vendeur = User.objects.get(username="vendeur_test")
        self.assertTrue(hasattr(vendeur, "vendor_profile"))

        # Étape 2 : Créer une catégorie et un produit
        categorie = Category.objects.create(name="Électronique")
        data_produit = {
            "name": "Nouveau Produit",
            "description": "Description produit",
            "price": "25.50",
            "category": categorie.id,
            "tags": "tech,électronique",
            "stock_quantity": "10",
            "is_active": True,
        }
        response = self.client.post(reverse("product_create"), data_produit)
        self.assertEqual(response.status_code, 302)

        produit = Product.objects.get(name="Nouveau Produit")
        self.assertEqual(produit.vendor, vendeur.vendor_profile)
        self.assertEqual(produit.price, 25.50)
