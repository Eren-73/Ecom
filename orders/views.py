# orders/views.py
# d:\Projets\Ecom\orders\views.py
# Ce fichier gère toutes les vues liées aux commandes et au panier
# WHY: Centraliser la logique métier pour le panier, checkout et historique des commandes
# RELEVANT FILES: orders/models.py, orders/templates/orders/*, products/models.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from accounts.models import CustomerProfile, VendorProfile
from django.conf import settings
from django.core.mail import send_mail


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Récupérer la quantité depuis le formulaire POST
    quantity = int(request.POST.get('quantity', 1))
    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # Si l'item existe déjà, on ajoute la quantité
        item.quantity += quantity
    else:
        # Si c'est un nouvel item, on définit la quantité
        item.quantity = quantity
    item.save()
    return redirect('cart')

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    """
    Gère le processus de checkout (simulation sans paiement réel)
    Crée une commande directement après validation du formulaire
    """
    cart = get_object_or_404(Cart, user=request.user)
    
    # Si le panier est vide, rediriger vers le panier
    if cart.items.count() == 0:
        messages.warning(request, 'Votre panier est vide.')
        return redirect('cart')

    if request.method == 'POST':
        # Récupérer les informations de livraison
        shipping_address = request.POST.get('shipping_address', '').strip()
        shipping_city = request.POST.get('shipping_city', '').strip()
        shipping_phone = request.POST.get('shipping_phone', '').strip()
        
        # Validation simple
        if not all([shipping_address, shipping_city, shipping_phone]):
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
            return render(request, 'orders/checkout.html', {'cart': cart})
        
        # Création de la commande (simulation de paiement réussi)
        order = Order.objects.create(
            customer=request.user,
            total_amount=cart.total_amount,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_phone=shipping_phone,
            status='confirmed'  # Statut confirmé directement (simulation)
        )
        
        # Créer les items de commande
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Vider le panier
        cart.items.all().delete()
        
        # Stocker l'ID de la commande dans la session pour l'afficher sur la page de succès
        request.session['last_order_id'] = order.pk
        
        # Message de succès
        messages.success(request, f'Commande #{order.pk} créée avec succès ! 🎉')
        
        # Rediriger vers la page de succès
        return redirect('payment_success')

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def payment(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)
    
    if request.method == 'POST':
        # On simule le paiement réussi
        order.status = 'confirmed'
        order.save()
        send_order_confirmation_email(request.user.email, order)
        return redirect('dashboard_customer')  # redirige vers le dashboard client

    return render(request, 'orders/payment.html', {'order': order})


@login_required
def payment_success(request):
    # Récupérer la dernière commande depuis la session
    last_order_id = request.session.get('last_order_id')
    order = None
    
    if last_order_id:
        order = Order.objects.filter(pk=last_order_id, customer=request.user).first()
        # Nettoyer la session après récupération
        del request.session['last_order_id']
    
    return render(request, 'orders/payment_success.html', {'order': order})

def send_order_confirmation_email(user_email, order):
    subject = f"Confirmation de votre commande #{order.pk}"
    message = f"""
Bonjour {order.customer.username},

Votre paiement a été effectué avec succès ✅
Voici le récapitulatif de votre commande :

Numéro de commande : {order.pk}
Montant total : {order.total_amount} €
Produits :
"""
    for item in order.items.all():
        message += f"- {item.product.name} x {item.quantity} : {item.price} €\n"

    message += "\nMerci pour votre confiance !"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


def boutique_vendeur(request, vendor_id):
    vendor = get_object_or_404(VendorProfile, id=vendor_id)
    products = vendor.products.filter(is_active=True)

    # Recherche par mot-clé
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'accounts/boutique_vendeur.html', {
        'vendor': vendor,
        'products': products,
        'query': query,
    })
