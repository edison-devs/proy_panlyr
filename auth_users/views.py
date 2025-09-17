from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin #Para autenticacion de usuario
from django.contrib.auth import authenticate,login, get_user_model,logout
from django.db import IntegrityError
from django.contrib import messages
from django.views import View
from .forms import LoginForm, RegisterForm # Importa el formulario forms.py

#------------------------------------------------------------------
# Login
#------------------------------------------------------------------
class UserLoginView(View):
    template_name= 'auth_users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        #Muestra el formulario del login vacio
        form=LoginForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        #Procesa el envio de formulario del login
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #Intenta autenticar el usuario
            user = authenticate(request, username=username, password=password)

            if user is not None:
                #Si las credenciales son validas inicia seción
                login(request, user)
                #Redirige a una pagina de exito (ej. La lista de secciones o el home.)
                return redirect('home') # Cambia esto a tu pagina de inicio deseada

            else:
                #Si las credenciales no son validas, Muestra un mensaje de error
                return render(request, self.template_name, {
                    'form':form,
                    'error_message': 'Nombre de usuario o contraseña incorrectos. '
                    })

        #Si es formulario no es valido (ej. campos vacios), lo vuelve a mostrar con errores
        return render(request, self.template_name, {'form': form})


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
        logout(request)
        return redirect('home')
