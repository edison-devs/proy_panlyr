from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin #Para autenticacion de usuario
from django.contrib.auth import authenticate,login, get_user_model,logout
from django.db import IntegrityError
from django.contrib import messages
from django.views import View
from .forms import LoginForm, RegisterForm # Importa el formulario forms.py
from django.contrib.admin.views.decorators import staff_member_required #Para manejar el cierre de secion del superadmin
from django.utils.decorators import method_decorator

#------------------------------------------------------------------
# Login
#------------------------------------------------------------------
class UserLoginView(View):
    template_name= 'auth_users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # Redirige según el Rol
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('superadmin_dashboard')
                elif user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('client_dashboard')

        return render(request, self.template_name, {
            'form': form,
            'error_message': 'Nombre de usuario o contraseña incorrectos.'
        })


#------------------------------------------------------------------
# Registro de usuario
#------------------------------------------------------------------
class UserRegisterView(View):
    template_name = 'auth_users/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User = get_user_model()
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
            except IntegrityError:
                messages.error(request, "⚠️ Ese usuario o correo ya está registrado.")
                return render(request, self.template_name, {'form': form})

            # Aquí ya NO iniciamos sesión automáticamente
            messages.success(request, "✅ Tu cuenta fue creada con éxito. Ahora puedes iniciar sesión.")
            return redirect('login')

        return render(request, self.template_name, {'form': form})



#------------------------------------------------------------------
# Logout
#------------------------------------------------------------------
#Redirige al home despues de iniciar o cerrar seción
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        is_super = request.user.is_superuser
        logout(request)
        return redirect('login' if is_super else 'home')



#------------------------------------------------------------------
# Logout del superadmin (para el panel Django)
#------------------------------------------------------------------

class AdminLogoutRedirectView(View):
    """Cierra la sesión del superadmin y redirige al login personalizado."""
    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

