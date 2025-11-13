"""
Tests unitaires pour les modèles de données (P1)
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import VendorProfile, CustomerProfile
from products.models import Product, Category
from orders.models import Order, OrderItem, Cart, CartItem


class TestProfilVendeur(TestCase):
    """Tests du modèle VendorProfile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="vendeur_test",
            email="vendeur@test.com",
            password="Test1234!",
        )

    def test_creation_profil_vendeur(self):
        """Création d'un profil vendeur"""
        vendeur = VendorProfile.objects.create(
            user=self.user,
            business_name="Ma Boutique Test",
            description="Description test",
            phone="0612345678",
            address="123 Rue Test",
            city="Paris",
        )

        self.assertIsNotNone(vendeur)
        self.assertEqual(vendeur.user, self.user)
        self.assertEqual(vendeur.business_name, "Ma Boutique Test")
        self.assertEqual(vendeur.is_verified, False)
        self.assertTrue(hasattr(self.user, "vendor_profile"))


class TestProfilClient(TestCase):
    """Tests du modèle CustomerProfile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="client_test",
            email="client@test.com",
            password="Test1234!",
        )

    def test_creation_profil_client_champs_optionnels(self):
        """Création profil client avec champs optionnels"""
        client = CustomerProfile.objects.create(user=self.user)

        self.assertIsNotNone(client)
        self.assertEqual(client.user, self.user)
        self.assertEqual(client.phone, "")
        self.assertEqual(client.address, "")
        self.assertEqual(client.city, "")


class TestProduit(TestCase):
    """Tests du modèle Product"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="vendeur_test",
            email="vendeur@test.com",
            password="Test1234!",
        )
        self.vendeur = VendorProfile.objects.create(
            user=self.user,
            business_name="Ma Boutique",
            description="Description",
            phone="0612345678",
            address="123 Rue Test",
            city="Paris",
        )
        self.categorie = Category.objects.create(
            name="Électronique",
            description="Catégorie test",
        )

    def test_propriete_stock_disponible(self):
        """Propriété is_in_stock"""
        produit_stock = Product.objects.create(
            vendor=self.vendeur,
            name="Produit En Stock",
            description="Description",
            price=10.50,
            category=self.categorie,
            stock_quantity=10,
        )
        produit_rupture = Product.objects.create(
            vendor=self.vendeur,
            name="Produit Rupture",
            description="Description",
            price=10.50,
            category=self.categorie,
            stock_quantity=0,
        )

        self.assertTrue(produit_stock.is_in_stock)
        self.assertFalse(produit_rupture.is_in_stock)

    def test_methode_liste_tags(self):
        """Méthode get_tags_list"""
        produit = Product.objects.create(
            vendor=self.vendeur,
            name="Produit Test",
            description="Description",
            price=10.50,
            category=self.categorie,
            tags="tag1, tag2 , tag3",
        )

        tags_list = produit.get_tags_list()
        self.assertEqual(tags_list, ["tag1", "tag2", "tag3"])

        produit_sans_tags = Product.objects.create(
            vendor=self.vendeur,
            name="Produit Sans Tags",
            description="Description",
            price=10.50,
            category=self.categorie,
            tags="",
        )
        self.assertEqual(produit_sans_tags.get_tags_list(), [])


class TestCommande(TestCase):
    """Tests du modèle Order"""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client_test",
            email="client@test.com",
            password="Test1234!",
        )

    def test_generation_numero_commande(self):
        """Génération automatique et unicité du numéro de commande"""
        commande1 = Order.objects.create(
            customer=self.client_user,
            total_amount=100.00,
            shipping_address="123 Rue Test",
            shipping_city="Paris",
            shipping_phone="0612345678",
        )
        commande2 = Order.objects.create(
            customer=self.client_user,
            total_amount=200.00,
            shipping_address="456 Rue Test",
            shipping_city="Lyon",
            shipping_phone="0698765432",
        )

        self.assertIsNotNone(commande1.order_number)
        self.assertEqual(len(commande1.order_number), 8)
        # Généré avec uuid4()[:8].upper(), donc unique et alphanumérique
        self.assertTrue(commande1.order_number.isalnum())
        self.assertNotEqual(commande1.order_number, commande2.order_number)
        self.assertEqual(commande1.status, "pending")


class TestArticleCommande(TestCase):
    """Tests du modèle OrderItem"""

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client_test",
            email="client@test.com",
            password="Test1234!",
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
            price=10.50,
            category=self.categorie,
        )
        self.commande = Order.objects.create(
            customer=self.client_user,
            total_amount=31.50,
            shipping_address="123 Rue",
            shipping_city="Paris",
            shipping_phone="0612345678",
        )

    def test_calcul_prix_total_article(self):
        """Propriété total_price d'un OrderItem"""
        article = OrderItem.objects.create(
            order=self.commande,
            product=self.produit,
            quantity=3,
            price=10.50,
        )

        total_attendu = 3 * 10.50
        self.assertEqual(float(article.total_price), total_attendu)


class TestPanier(TestCase):
    """Tests du modèle Cart"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="client_test",
            email="client@test.com",
            password="Test1234!",
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
            description="Desc",
            price=10.00,
            category=self.categorie,
        )
        self.produit2 = Product.objects.create(
            vendor=self.vendeur,
            name="Produit 2",
            description="Desc",
            price=15.00,
            category=self.categorie,
        )

    def test_calcul_total_panier(self):
        """Propriété total_amount du panier"""
        panier = Cart.objects.create(user=self.user)
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

        total_attendu = (2 * 10.00) + (1 * 15.00)
        self.assertEqual(float(panier.total_amount), total_attendu)


class TestArticlePanier(TestCase):
    """Tests du modèle CartItem"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="client_test",
            email="client@test.com",
            password="Test1234!",
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
            price=12.50,
            category=self.categorie,
        )
        self.panier = Cart.objects.create(user=self.user)

    def test_calcul_prix_total_article_panier(self):
        """Propriété total_price d'un CartItem"""
        article = CartItem.objects.create(
            cart=self.panier,
            product=self.produit,
            quantity=4,
        )

        total_attendu = 4 * 12.50
        self.assertEqual(float(article.total_price), total_attendu)
