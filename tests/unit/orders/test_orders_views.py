"""
Tests fonctionnels pour le module Orders (P1)
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import VendorProfile
from products.models import Product, Category
from orders.models import Cart, CartItem, Order


class TestAjoutPanier(TestCase):
    """Tests d'ajout au panier"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="client_test", password="Test1234!"
        )
        self.vendeur = VendorProfile.objects.create(
            user=User.objects.create_user(username="vendeur", password="test"),
            business_name="Boutique",
            description="Desc",
            phone="0612345678",
            address="123 Rue",
            city="Paris",
        )
        self.categorie = Category.objects.create(name="Catégorie")
        self.produit = Product.objects.create(
            vendor=self.vendeur,
            name="Produit Test",
            description="Description",
            price=10.00,
            category=self.categorie,
        )

    def test_ajout_produit_au_panier(self):
        """Ajout d'un nouveau produit au panier"""
        self.client.login(username="client_test", password="Test1234!")
        url_ajout = reverse("add_to_cart", kwargs={"product_id": self.produit.pk})

        response = self.client.post(url_ajout, {"quantity": 2})

        self.assertEqual(response.status_code, 302)
        panier = Cart.objects.get(user=self.user)
        article = CartItem.objects.get(cart=panier, product=self.produit)
        self.assertEqual(article.quantity, 2)
        self.assertRedirects(response, reverse("cart"))


class TestAffichagePanier(TestCase):
    """Tests d'affichage panier"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="client_test", password="Test1234!"
        )
        self.vendeur = VendorProfile.objects.create(
            user=User.objects.create_user(username="vendeur", password="test"),
            business_name="Boutique",
            description="Desc",
            phone="0612345678",
            address="123 Rue",
            city="Paris",
        )
        self.categorie = Category.objects.create(name="Catégorie")
        self.produit1 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 1",
            description="Description",
            price=10.00,
            category=self.categorie,
        )
        self.produit2 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 2",
            description="Description",
            price=15.00,
            category=self.categorie,
        )

    def test_affichage_panier_avec_articles(self):
        """Affichage panier avec articles"""
        self.client.login(username="client_test", password="Test1234!")
        panier = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=panier, product=self.produit1, quantity=2)
        CartItem.objects.create(cart=panier, product=self.produit2, quantity=1)

        response = self.client.get(reverse("cart"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("cart", response.context)
        panier = response.context["cart"]
        total_attendu = (2 * 10.00) + (1 * 15.00)
        self.assertEqual(float(panier.total_amount), total_attendu)
        self.assertEqual(panier.total_items, 3)


class TestCheckout(TestCase):
    """Tests de checkout"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="client_test", password="Test1234!"
        )
        self.vendeur = VendorProfile.objects.create(
            user=User.objects.create_user(username="vendeur", password="test"),
            business_name="Boutique",
            description="Desc",
            phone="0612345678",
            address="123 Rue",
            city="Paris",
        )
        self.categorie = Category.objects.create(name="Catégorie")
        self.produit1 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 1",
            description="Description",
            price=10.00,
            category=self.categorie,
        )
        self.produit2 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 2",
            description="Description",
            price=20.00,
            category=self.categorie,
        )

    def test_checkout_reussi(self):
        """Checkout réussi - Création commande"""
        self.client.login(username="client_test", password="Test1234!")
        panier = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=panier, product=self.produit1, quantity=2)
        CartItem.objects.create(cart=panier, product=self.produit2, quantity=1)

        data_checkout = {
            "shipping_address": "123 Rue Test",
            "shipping_city": "Paris",
            "shipping_phone": "0612345678",
        }

        response = self.client.post(reverse("checkout"), data_checkout)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(customer=self.user).exists())

        commande = Order.objects.get(customer=self.user)
        self.assertEqual(commande.status, "confirmed")
        self.assertEqual(float(commande.total_amount), 40.00)
        self.assertIsNotNone(commande.order_number)
        self.assertEqual(commande.items.count(), 2)
        self.assertEqual(panier.items.count(), 0)
        self.assertRedirects(response, reverse("payment_success"))
