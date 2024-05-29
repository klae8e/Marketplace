from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Category, Brand, Model, Color, Storage, SellerProduct


class RegisterForm(UserCreationForm):
    pass

class SellerProductForm(forms.ModelForm):
    class Meta:
        model = SellerProduct
        fields = ['category', 'brand', 'model', 'color', 'storage', 'price', 'quantity', 'description']
        labels = {
            'category': 'Category',
            'brand': 'Brand',
            'model': 'Model',
            'color': 'Color',
            'storage': 'Storage',
            'price': 'Price',
            'quantity': 'Quantity',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Поиск')


