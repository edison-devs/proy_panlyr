#mi_app/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm, UserCreationForm



User = get_user_model() #Obtiene el modelo de usuario activo (tu usuario personalizado)

class LoginForm(forms.Form):
	username = forms.CharField(
	label= "Nombre de Usuario",
	max_length=150,
	widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario','class': 'form-control'})
	)

	password = forms.CharField(
	label= "Contraseña",
	widget=forms.PasswordInput(attrs={'placeholder': 'Tu Contraseña',  'class': 'form-control'})
	)


class RegisterForm(forms.Form):
	username = forms.CharField(
	label= "Nombre de Usuario",
	max_length=150,
	widget=forms.TextInput(attrs={'placeholder': 'Define nombre de usuario',  'class': 'form-control'})
	)

	email = forms.EmailField(
		label="correo electrónico",
		widget=forms.EmailInput(attrs={'placeholder':'tu@gmail.com',  'class': 'form-control'})

	)
	
	password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce tu Contraseña',  'class': 'form-control'})
    )

	
	password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite tu Contraseña',  'class': 'form-control'})
    )

    
    # validaciones de username y email sin cambios
	def clean_username(self):
		# validación para asegurar que el nombre de usuario no exista
		username = self.cleaned_data['username']
		
		if User.objects.filter(username=username).exists():
			raise ValidationError ("Este nombre de usuario ya esta en uso.")
		return username
	
	def clean_email(self):
		# validación para asegurar que el email no exista
		email = self.cleaned_data['email']
		
		if User.objects.filter(email=email).exists():
			raise ValidationError ("Este correo electronico ya esta registrado.")
		return email


	def clean(self):
		cleaned_data     = super().clean()
		password         = cleaned_data.get('password')
		password_confirm = cleaned_data.get('password_confirm')

        # Asegura de que ambos campos estén presentes y, si no coinciden, lanzar el error
		if password and password_confirm and password != password_confirm:
            # Asignamos el error al campo password_confirm
			self.add_error('password_confirm', "Las contraseñas no coinciden.")
        
		return cleaned_data


# -------------------------
# Formulario para Admin (edición de usuarios)
# -------------------------
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")

        # 🔒 Lógica de roles → aplicar directamente al objeto
        if role == "cliente":
            self.instance.is_staff = False
            self.instance.is_superuser = False
        elif role == "admin":
            self.instance.is_superuser = False

        return cleaned_data

