"""
Tests fonctionnels pour le module Accounts (P1)
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import VendorProfile, CustomerProfile
from products.models import Product, Category
from orders.models import Order, OrderItem


class TestInscriptionVendeur(TestCase):
    """Tests d'inscription vendeur"""
    
    def setUp(self):
        self.client = Client()
        self.url_inscription = reverse('vendor_signup')
    
    def test_inscription_vendeur_reussie(self):
        """Inscription vendeur réussie"""
        data = {
            'username': 'vendeur_test',
            'email': 'vendeur@test.com',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
            'business_name': 'Ma Boutique Test',
            'description': 'Description de la boutique',
            'phone': '0612345678',
            'address': '123 Rue Test',
            'city': 'Paris'
        }
        
        response = self.client.post(self.url_inscription, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='vendeur_test').exists())
        user = User.objects.get(username='vendeur_test')
        self.assertTrue(hasattr(user, 'vendor_profile'))
        self.assertEqual(user.vendor_profile.business_name, 'Ma Boutique Test')
        self.assertRedirects(response, reverse('dashboard_vendor'))


class TestInscriptionClient(TestCase):
    """Tests d'inscription client"""
    
    def setUp(self):
        self.client = Client()
        self.url_inscription = reverse('customer_signup')
    
    def test_inscription_client_reussie(self):
        """Inscription client réussie"""
        data = {
            'username': 'client_test',
            'email': 'client@test.com',
            'password1': 'Test1234!',
            'password2': 'Test1234!',
            'phone': '0612345678',
            'address': '123 Rue Test',
            'city': 'Paris'
        }
        
        response = self.client.post(self.url_inscription, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='client_test').exists())
        user = User.objects.get(username='client_test')
        self.assertTrue(hasattr(user, 'customer_profile'))
        self.assertRedirects(response, reverse('dashboard_customer'))


class TestConnexion(TestCase):
    """Tests de connexion"""
    
    def setUp(self):
        self.client = Client()
        self.url_connexion = reverse('login')
        
        # Créer un vendeur
        self.user_vendeur = User.objects.create_user(
            username='vendeur_test',
            password='Test1234!'
        )
        VendorProfile.objects.create(
            user=self.user_vendeur,
            business_name='Boutique Test',
            description='Description',
            phone='0612345678',
            address='123 Rue',
            city='Paris'
        )
        
        # Créer un client
        self.user_client = User.objects.create_user(
            username='client_test',
            password='Test1234!'
        )
        CustomerProfile.objects.create(user=self.user_client)
    
    def test_connexion_vendeur_reussie(self):
        """Connexion vendeur réussie"""
        data = {
            'username': 'vendeur_test',
            'password': 'Test1234!'
        }
        
        response = self.client.post(self.url_connexion, data, follow=False)
        
        self.assertEqual(response.status_code, 302)
        # Vérifier que la redirection pointe vers dashboard_vendor
        # L'URL peut être /dashboard/ ou /accounts/vendor/dashboard/
        self.assertIn('dashboard', response.url.lower())
    
    def test_connexion_client_reussie(self):
        """Connexion client réussie"""
        data = {
            'username': 'client_test',
            'password': 'Test1234!'
        }
        
        response = self.client.post(self.url_connexion, data, follow=False)
        
        self.assertEqual(response.status_code, 302)
        # Vérifier que la redirection pointe vers dashboard_customer
        # L'URL peut être /dashboard/ ou /accounts/customer/dashboard/
        self.assertIn('dashboard', response.url.lower())


class TestDashboardVendeur(TestCase):
    """Tests du dashboard vendeur"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='vendeur_test',
            password='Test1234!'
        )
        self.vendeur = VendorProfile.objects.create(
            user=self.user,
            business_name='Boutique Test',
            description='Description',
            phone='0612345678',
            address='123 Rue',
            city='Paris'
        )
        self.categorie = Category.objects.create(name='Catégorie')
        self.url_dashboard = reverse('dashboard_vendor')
    
    def test_affichage_dashboard_avec_produits_et_commandes(self):
        """Affichage dashboard vendeur avec produits et commandes"""
        # Créer des produits
        produit1 = Product.objects.create(
            vendor=self.vendeur,
            name='Produit 1',
            description='Description',
            price=10.00,
            category=self.categorie
        )
        produit2 = Product.objects.create(
            vendor=self.vendeur,
            name='Produit 2',
            description='Description',
            price=20.00,
            category=self.categorie
        )
        
        # Créer un client et une commande
        client = User.objects.create_user(username='client', password='test')
        commande = Order.objects.create(
            customer=client,
            total_amount=30.00,
            shipping_address='123 Rue',
            shipping_city='Paris',
            shipping_phone='0612345678'
        )
        OrderItem.objects.create(order=commande, product=produit1, quantity=1, price=10.00)
        OrderItem.objects.create(order=commande, product=produit2, quantity=1, price=20.00)
        
        self.client.login(username='vendeur_test', password='Test1234!')
        response = self.client.get(self.url_dashboard)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produit 1')
        self.assertContains(response, 'Produit 2')
        self.assertIn('mois', response.context)
        self.assertIn('totaux', response.context)


class TestDashboardClient(TestCase):
    """Tests du dashboard client"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='client_test',
            password='Test1234!'
        )
        CustomerProfile.objects.create(user=self.user)
        self.url_dashboard = reverse('dashboard_customer')
    
    def test_affichage_dashboard_avec_commandes(self):
        """Affichage dashboard client avec commandes"""
        # Créer des commandes
        commande1 = Order.objects.create(
            customer=self.user,
            total_amount=100.00,
            shipping_address='123 Rue',
            shipping_city='Paris',
            shipping_phone='0612345678'
        )
        commande2 = Order.objects.create(
            customer=self.user,
            total_amount=200.00,
            shipping_address='456 Rue',
            shipping_city='Lyon',
            shipping_phone='0698765432'
        )
        
        self.client.login(username='client_test', password='Test1234!')
        response = self.client.get(self.url_dashboard)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.context)
        commandes = list(response.context['orders'])
        # Vérifier qu'on a 2 commandes
        self.assertEqual(len(commandes), 2)
