from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product
from accounts.models import CustomerProfile

class Order(models.Model):
    """Modèle des commandes"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('processing', 'En traitement'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Client")
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de commande")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    
    # Adresse de livraison
    shipping_address = models.TextField(verbose_name="Adresse de livraison")
    shipping_city = models.CharField(max_length=100, verbose_name="Ville de livraison")
    shipping_phone = models.CharField(max_length=20, verbose_name="Téléphone de livraison")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de livraison")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande #{self.order_number} - {self.customer.username}"

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Générer un numéro de commande unique
            import uuid
            self.order_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Articles dans une commande"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    
    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.price


class Cart(models.Model):
    """Panier d'achat"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.user.username}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Articles dans le panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Panier")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price
