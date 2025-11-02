# ecommerce_platform/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import VendorProfile, CustomerProfile
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Vérifier le rôle et rediriger
            if hasattr(user, 'customer_profile'):
                return redirect('dashboard_customer')
            elif hasattr(user, 'vendor_profile'):
                return redirect('dashboard_vendor')
            else:
                return redirect('/admin/')  # Admin

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def client_dashboard(request):
    return render(request, 'accounts/dashboard_customer.html')


@login_required
def vendeur_dashboard(request):
    return render(request, 'accounts/dashboard_vendor.html')

@login_required
def redirect_dashboard(request):
    if hasattr(request.user, 'vendor_profile'):
        return redirect('dashboard_vendor')
    elif hasattr(request.user, 'customer_profile'):
        return redirect('dashboard_customer')
    else:
        return redirect('home')