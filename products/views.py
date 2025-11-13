from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageFormSet, CategoryForm
from django.contrib import messages

@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    selected_tag = request.GET.get('tag', '')

    if selected_category:
        products = products.filter(category_id=selected_category)
    if selected_tag:
        products = products.filter(tags__icontains=selected_tag)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_create(request):
    # Récupération du profil vendeur associé à l'utilisateur connecté
    vendor = request.user.vendor_profile  

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor  # assignation du vendeur
            product.save()

            # Gestion des images supplémentaires si besoin
            for f in request.FILES.getlist('additional_images'):
                ProductImage.objects.create(product=product, image=f)

            messages.success(request, f"Produit '{product.name}' créé avec succès ! ✅")
            return redirect('dashboard_vendor')
        else:
            messages.error(request, "Erreur : veuillez corriger les champs ci-dessous.")
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form, 'title': 'Ajouter un produit'})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user.vendor_profile)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Produit modifié avec succès !")
            return redirect('dashboard_vendor')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'formset': formset})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user.vendor_profile)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Produit supprimé avec succès !")
        return redirect('dashboard_vendor')
    return render(request, 'products/product_confirm_delete.html', {'product': product})



# Liste des catégories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

# Création
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie créée avec succès !")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})

# Modification
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie modifiée avec succès !")
            return redirect('category/category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form})

# Suppression
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Catégorie supprimée avec succès !")
        return redirect('category_list')
    return render(request, 'category/category_confirm_delete.html', {'category': category})
