# accounts/forms.py
# d:\Projets\Ecom\accounts\forms.py
# Formulaires pour l'inscription et connexion des utilisateurs
# WHY: Gérer la création de comptes vendeurs et clients avec validation
# RELEVANT FILES: accounts/views.py, accounts/models.py, accounts/templates/accounts/*

from django import forms
from django.contrib.auth.models import User
from .models import VendorProfile, CustomerProfile
from django.contrib.auth.forms import AuthenticationForm

class VendorSignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

class CustomerSignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['business_name', 'description', 'phone', 'address', 'city', 'image']
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de votre boutique',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Décrivez votre boutique et vos produits...', 
                'rows': 4,
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: 0612345678',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse complète de votre entreprise',
                'rows': 3,
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ville',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'business_name': "Nom de l'entreprise",
            'description': 'Description de la boutique',
            'phone': 'Téléphone',
            'address': "Adresse de l'entreprise",
            'city': 'Ville',
            'image': 'Logo de la boutique (optionnel)',
        }

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'city']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: 0612345678'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse complète',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ville'
            }),
        }
        labels = {
            'phone': 'Téléphone',
            'address': 'Adresse',
            'city': 'Ville',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))