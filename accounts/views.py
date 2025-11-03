import csv
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from accounts.models import VendorProfile
from products.models import Product
from .forms import VendorSignUpForm, CustomerSignUpForm, VendorProfileForm, CustomerProfileForm
from orders.models import Cart, OrderItem,Order
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count


# -------------------
# Signup
# -------------------
def vendor_signup(request):
    if request.method == 'POST':
        user_form = VendorSignUpForm(request.POST)
        profile_form = VendorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('dashboard_vendor')
    else:
        user_form = VendorSignUpForm()
        profile_form = VendorProfileForm()
    return render(request, 'accounts/vendor_signup.html', {'user_form': user_form, 'profile_form': profile_form})


def customer_signup(request):
    if request.method == 'POST':
        user_form = CustomerSignUpForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('dashboard_customer')
    else:
        user_form = CustomerSignUpForm()
        profile_form = CustomerProfileForm()
    return render(request, 'accounts/customer_signup.html', {'user_form': user_form, 'profile_form': profile_form})


# -------------------
# Login / Logout
# -------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirection selon rôle
            if hasattr(user, 'vendor_profile'):
                return redirect('dashboard_vendor')
            elif hasattr(user, 'customer_profile'):
                return redirect('dashboard_customer')
            else:
                messages.error(request, "Profil introuvable.")
                logout(request)
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------
# Dashboards
# -------------------
@login_required
def dashboard_vendor(request):
    # Récupérer les produits du vendeur
    products = request.user.vendor_profile.products.all()

    # Récupérer tous les OrderItems correspondant aux produits du vendeur
    order_items = OrderItem.objects.filter(product__in=products).select_related('order', 'product')

    # ✅ Statistiques : ventes par mois
    ventes_par_mois = (
        order_items.values_list('order__created_at__month')
        .annotate(total=Sum('product__price'))
        .order_by('order__created_at__month')
    )
    mois = [f"Mois {m[0]}" for m in ventes_par_mois]
    totaux = [float(m[1]) for m in ventes_par_mois]

    # ✅ Produits les plus vendus
    produits_top = (
        order_items.values('product__name')
        .annotate(qte=Count('product'))
        .order_by('-qte')[:5]
    )
    noms_produits = [p['product__name'] for p in produits_top]
    qte_vendue = [p['qte'] for p in produits_top]

    # ⚡ Convertir en JSON pour Chart.js
    context = {
        'products': products,
        'order_items': order_items,
        'mois': json.dumps(mois),
        'totaux': json.dumps(totaux),
        'noms_produits': json.dumps(noms_produits),
        'qte_vendue': json.dumps(qte_vendue),
    }

    return render(request, 'accounts/dashboard_vendor.html', context)


@login_required
def dashboard_customer(request):
    return render(request, 'accounts/dashboard_customer.html')

@login_required
def change_order_status(request, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order_item.order.status = new_status
            order_item.order.save()
    return redirect('dashboard_vendor')

@login_required
def update_order_status(request, order_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Méthode non autorisée"}, status=400)


@login_required
def dashboard_customer(request):
    # Récupère toutes les commandes du client connecté
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    # Récupère le panier du client (optionnel)
    cart = None
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        pass

    context = {
        'orders': orders,
        'cart': cart
    }
    return render(request, 'accounts/dashboard_customer.html', context)


@login_required
def order_detail_customer(request, order_id):
    # Récupère la commande du client
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    
    # Récupère les items de la commande
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items
    }
    return render(request, 'accounts/order_detail_customer.html', context)


@login_required
def sales_by_product(request, product_id):
    if product_id == "Tous":
        order_items = OrderItem.objects.filter(product__vendor=request.user.vendor_profile)
    else:
        order_items = OrderItem.objects.filter(product__id=product_id)

    ventes_par_mois = (
        order_items.values_list('order__created_at__month')
        .annotate(total=Sum('price'))
        .order_by('order__created_at__month')
    )

    labels = [f"Mois {m[0]}" for m in ventes_par_mois]
    data = [float(m[1]) for m in ventes_par_mois]

    return JsonResponse({'labels': labels, 'data': data})

@login_required
def vendor_sales_csv(request):
    products = request.user.vendor_profile.products.all()
    order_items = OrderItem.objects.filter(product__in=products)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ventes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Commande', 'Produit', 'Quantité', 'Prix unitaire', 'Sous-total', 'Client', 'Statut'])
    for item in order_items:
        writer.writerow([item.order.order_number, item.product.name, item.quantity,
                         item.price, item.total_price, item.order.customer.username, item.order.status])
    return response


def liste_boutiques(request):
    boutiques = VendorProfile.objects.filter(is_verified=True)
    return render(request, 'accounts/liste_boutiques.html', {'boutiques': boutiques})

def boutique_vendeur(request, vendor_id):
    vendor = get_object_or_404(VendorProfile, pk=vendor_id)
    products = Product.objects.filter(vendor=vendor, is_active=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'accounts/boutique_vendeur.html', {
        'vendor': vendor,
        'products': products,
        'query': query
    })