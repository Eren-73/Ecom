"""
Tests d'intégration - Interactions entre modules (P1)
Vérifie que les modules interagissent correctement
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import VendorProfile, CustomerProfile
from products.models import Product, Category
from orders.models import Cart, CartItem, Order, OrderItem


class TestIntegrationAccountsProducts(TestCase):
    """Tests d'intégration entre Accounts et Products"""

    def setUp(self):
        self.user_vendeur = User.objects.create_user(
            username="vendeur",
            password="test",
        )
        self.vendeur = VendorProfile.objects.create(
            user=self.user_vendeur,
            business_name="Boutique",
            description="Desc",
            phone="0612345678",
            address="123 Rue",
            city="Paris",
        )
        self.categorie = Category.objects.create(name="Catégorie")

    def test_relation_vendeur_produit(self):
        """Relation vendeur-produit"""
        produit = Product.objects.create(
            vendor=self.vendeur,
            name="Produit",
            description="Desc",
            price=10.00,
            category=self.categorie,
        )

        self.assertIn(produit, self.vendeur.products.all())
        self.assertEqual(produit.vendor, self.vendeur)


class TestIntegrationProductsOrders(TestCase):
    """Tests d'intégration entre Products et Orders"""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client",
            password="test",
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
            name="Produit",
            description="Desc",
            price=10.00,
            category=self.categorie,
        )

    def test_panier_avec_produits(self):
        """Panier avec produits"""
        panier = Cart.objects.create(user=self.client_user)
        article = CartItem.objects.create(
            cart=panier,
            product=self.produit,
            quantity=3,
        )

        total_attendu = 3 * self.produit.price
        self.assertEqual(float(panier.total_amount), float(total_attendu))
        self.assertEqual(article.product, self.produit)

    def test_commande_avec_produits(self):
        """Commande avec produits"""
        commande = Order.objects.create(
            customer=self.client_user,
            total_amount=30.00,
            shipping_address="123 Rue",
            shipping_city="Paris",
            shipping_phone="0612345678",
        )
        article = OrderItem.objects.create(
            order=commande,
            product=self.produit,
            quantity=3,
            price=self.produit.price,
        )

        self.assertEqual(article.product, self.produit)
        self.assertIn(article, commande.items.all())
        self.assertEqual(
            article.total_price,
            3 * self.produit.price,
        )


class TestIntegrationAccountsOrders(TestCase):
    """Tests d'intégration entre Accounts et Orders"""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client",
            password="test",
        )
        CustomerProfile.objects.create(user=self.client_user)

    def test_relation_client_panier(self):
        """Relation client-panier"""
        panier = Cart.objects.create(user=self.client_user)

        self.assertEqual(self.client_user.cart, panier)
        self.assertEqual(panier.user, self.client_user)

    def test_relation_client_commandes(self):
        """Relation client-commandes"""
        commande1 = Order.objects.create(
            customer=self.client_user,
            total_amount=10.00,
            shipping_address="123 Rue",
            shipping_city="Paris",
            shipping_phone="0612345678",
        )
        commande2 = Order.objects.create(
            customer=self.client_user,
            total_amount=20.00,
            shipping_address="456 Rue",
            shipping_city="Lyon",
            shipping_phone="0698765432",
        )

        commandes_client = self.client_user.orders.all()
        self.assertEqual(commandes_client.count(), 2)
        self.assertIn(commande1, commandes_client)
        self.assertIn(commande2, commandes_client)


class TestIntegrationComplete(TestCase):
    """Test d'intégration complet : Tous les modules ensemble"""

    def setUp(self):
        # Créer un vendeur
        vendeur_user = User.objects.create_user(
            username="vendeur",
            password="test",
        )
        self.vendeur = VendorProfile.objects.create(
            user=vendeur_user,
            business_name="Boutique",
            description="Desc",
            phone="0612345678",
            address="123 Rue",
            city="Paris",
        )

        # Créer un client
        self.client_user = User.objects.create_user(
            username="client",
            password="test",
        )
        CustomerProfile.objects.create(user=self.client_user)

        # Créer une catégorie et des produits
        self.categorie = Category.objects.create(name="Catégorie")
        self.produit1 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 1",
            description="Desc",
            price=10.00,
            category=self.categorie,
        )
        self.produit2 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 2",
            description="Desc",
            price=20.00,
            category=self.categorie,
        )

    def test_integration_complete(self):
        """Intégration complète : Vendeur → Produits → Client → Panier → Commande"""
        # Vérifier que le vendeur a des produits
        self.assertEqual(self.vendeur.products.count(), 2)

        # Créer un panier pour le client
        panier = Cart.objects.create(user=self.client_user)
        CartItem.objects.create(
            cart=panier,
            product=self.produit1,
            quantity=2,
        )
        CartItem.objects.create(
            cart=panier,
            product=self.produit2,
            quantity=1,
        )

        # Vérifier le total du panier
        self.assertEqual(float(panier.total_amount), 40.00)

        # Créer une commande
        commande = Order.objects.create(
            customer=self.client_user,
            total_amount=panier.total_amount,
            shipping_address="123 Rue",
            shipping_city="Paris",
            shipping_phone="0612345678",
        )

        # Créer les OrderItems
        for article in panier.items.all():
            OrderItem.objects.create(
                order=commande,
                product=article.product,
                quantity=article.quantity,
                price=article.product.price,
            )

        # Vérifier l'intégration complète
        self.assertEqual(commande.customer, self.client_user)
        self.assertIn(commande, self.client_user.orders.all())
        self.assertEqual(commande.items.count(), 2)
        for article in commande.items.all():
            self.assertEqual(article.order, commande)
            self.assertIn(
                article.product,
                [self.produit1, self.produit2],
            )
            self.assertEqual(article.product.vendor, self.vendeur)
