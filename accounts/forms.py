# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import VendorProfile, CustomerProfile
from django.contrib.auth.forms import AuthenticationForm

class VendorSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['business_name', 'description', 'phone', 'address', 'city']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'city']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))