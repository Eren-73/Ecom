from django.db import models
from django.contrib.auth.models import User
# This line imports the built-in User model from Django's authentication system. It allows us to use the User model in our models for things like associating data with a specific user.
from django.urls import reverse

class VendorProfile(models.Model):
    """Profil des vendeurs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=200, verbose_name="Nom de l'entreprise")
    description = models.TextField(verbose_name="Description de l'entreprise")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    is_verified = models.BooleanField(default=False, verbose_name="Vérifié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Vendeur"
        verbose_name_plural = "Profils Vendeurs"

    def __str__(self):
        return f"{self.business_name} - {self.user.username}"

    def get_absolute_url(self):
        return reverse('vendor_detail', kwargs={'pk': self.pk})


class CustomerProfile(models.Model):
    """Profil des clients"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True)
    address = models.TextField(verbose_name="Adresse", blank=True)
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Client"
        verbose_name_plural = "Profils Clients"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.username}"
