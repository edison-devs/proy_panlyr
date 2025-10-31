#mi_app/forms.py
from django import forms
from django.core.exceptions import ValidationError

class Category(forms.Form):
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el nombre de la categoría'
        })
    )
    
    description = forms.CharField(
        label="Descripción", 
        widget=forms.Textarea(attrs={
            'placeholder': 'Ingrese la descripción',
            'rows': 4
        }),
        required=False
    )

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        
        if description and len(description) < 10:
            raise ValidationError("La descripción debe tener al menos 10 caracteres.")
            
        return description