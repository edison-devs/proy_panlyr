# core/forms.py
from django import forms
from .models import Product, PaymentMethod, Order



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "price", "description", "image"]

        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
#class CartProductForm(forms.ModelForm):
    #class Meta:
        #model = CartProduct
        #fields = ['product', 'quantity']

class PedidoForm(forms.Form):
    metodo_pago = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(deleted_at__isnull=True), 
        label="Método de pago",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    direccion = forms.CharField(
        max_length=255, 
        label="Dirección de entrega",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese la dirección de entrega"})
    )


class ComprobantePagoForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comprobante_pago']
        widgets = {
            'comprobante_pago': forms.FileInput(attrs={
                "class": "form-control",
                "accept": ".jpg,.jpeg,.png,.pdf,.webp"
            })
        }
        labels = {
            'comprobante_pago': 'Comprobante de pago'
        }