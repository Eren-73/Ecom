# ecommerce_platform/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import VendorProfile, CustomerProfile
from django.contrib.auth.models import User
from products.models import Product,Category




def home(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')

    # Produits filtrés
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Catégories
    categories = Category.objects.all()

    # Boutiques activées (is_verified=True)
    boutiques = VendorProfile.objects.filter(is_verified=True)

    # Préparer les produits mis en avant par boutique (max 5 par boutique)
    boutiques_products = []
    for vendor in boutiques:
        vendor_products = Product.objects.filter(vendor=vendor)[:5]  # 5 produits max
        boutiques_products.append({'vendor': vendor, 'products': vendor_products})

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'boutiques': boutiques,
        'boutiques_products': boutiques_products,
    }
    return render(request, 'home.html', context)

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
    

def liste_boutiques(request):
    boutiques = VendorProfile.objects.filter(is_verified=True)  # seulement les boutiques vérifiées
    return render(request, 'accounts/liste_boutiques.html', {
        'boutiques': boutiques
    })