from django import forms
from .models import Product, Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        