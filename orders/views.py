# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import stripe
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from accounts.models import CustomerProfile, VendorProfile
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.count() == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        # Création de la commande
        order = Order.objects.create(
            customer=request.user,
            total_amount=cart.total_amount,
            shipping_address=request.POST['shipping_address'],
            shipping_city=request.POST['shipping_city'],
            shipping_phone=request.POST['shipping_phone']
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Vider le panier
        cart.items.all().delete()
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        return redirect('home')

    # Création d'une session Stripe
    if request.method == 'POST':
        line_items = []
        for item in cart.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),  # Stripe attend des centimes
                },
                'quantity': item.quantity,
            })
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/orders/success/'),
            cancel_url=request.build_absolute_uri('/orders/checkout/'),
        )
        return redirect(session.url, code=303)

    cart_items = cart.items.all()
    total_amount = cart.total_amount

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

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
    # Vider le panier de l'utilisateur
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()

    return render(request, 'orders/payment_success.html')

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