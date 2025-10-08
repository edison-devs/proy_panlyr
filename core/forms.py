# core/forms.py
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "price", "description", "stock", "image"]

        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
