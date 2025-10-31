# core/forms.py
from django import forms
from .models import Product
from .models import CartProduct, Product
from .models import Product, PaymentMethod, OrderType



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
#class CartProductForm(forms.ModelForm):
    #class Meta:
        #model = CartProduct
        #fields = ['product', 'quantity']

class PedidoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Product.objects.filter(stock__gt=0), label="Producto")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")
    metodo_pago = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), label="Método de pago")
    tipo_pedido = forms.ModelChoiceField(queryset=OrderType.objects.all(), label="Tipo de pedido")
    direccion = forms.CharField(max_length=255, label="Dirección de entrega")