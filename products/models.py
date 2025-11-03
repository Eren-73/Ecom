from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import VendorProfile

class Category(models.Model):
    """Catégories de produits"""
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Modèle des produits"""
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='products', verbose_name="Vendeur")
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Catégorie")
    tags = models.CharField(max_length=500, blank=True, verbose_name="Étiquettes (séparées par des virgules)")
<<<<<<< HEAD
    image = models.ImageField(upload_to='products/', verbose_name="Image principale")
=======
    image = models.ImageField(upload_to='products/', blank=True, null=True,verbose_name="Image principale")
>>>>>>> feature/produits
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    def get_tags_list(self):
        """Retourne les étiquettes sous forme de liste"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class ProductImage(models.Model):
    """Images supplémentaires des produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='products/additional/')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texte alternatif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image supplémentaire"
        verbose_name_plural = "Images supplémentaires"

    def __str__(self):
        return f"Image pour {self.product.name}"
