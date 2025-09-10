from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin #Para autenticacion de usuario
from django.contrib.auth import authenticate,login, get_user_model,logout
from django.views import View
from django.contrib import messages
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
        #Muestra el formulario de registro vacío
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        # Procesa el envío del formulario de registro}
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Crea el nuevo usuario
            # Usar create_user() es una buena práctica para manejar contraseñas
            # o directamente crear y luego set_password()
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)

            # Opcional: Iniciar sesión al usuario automáticamente después del registro
            login(request, user)


            #Redirige a una pagina de exito (ej. el home o el dashboard del usuario)
            return redirect('login') # Cambia esto a tu pagina de inicio o dashboard
        
        # Si el formulario no es valido lo vuelve a mostrar con errores
        return render(request, self.template_name, {'form':form})   
    

#Redirige al home despues de iniciar o cerrar seción
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
