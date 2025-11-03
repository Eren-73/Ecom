from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category', 'tags',
            'stock_quantity', 'image', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nom du produit'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Description détaillée', 'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Prix en €'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Tags séparés par des virgules'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Quantité en stock'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texte alternatif'}),
        }


# Formset pour gérer plusieurs images supplémentaires
ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm,
    extra=3, can_delete=True
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la catégorie'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
