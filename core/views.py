# View de app core logica principal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin #Para autenticacion de usuario
from django.contrib.auth import authenticate,login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages                      # <- necesario para mostrar mensajes
from .models import *
from .forms import ProductForm
from django.shortcuts import render



# Create your views here.

#placeholder vistas sencillas para mas adelante estilizar:

@login_required
def product_catalog(request):
    return render(request, 'core/catalogo.html')

@login_required
def pedidos_list(request):
    return render(request, 'core/placeholders/pedidos_list.html')

@login_required
def papelera(request):
    return render(request, 'core/placeholders/papelera.html')

@login_required
def carrito(request):
    return render(request, 'core/placeholders/carrito.html')

@login_required
def mis_pedidos(request):
    return render(request, 'core/placeholders/mis_pedidos.html')

@login_required
def reportes(request):
    return render(request, 'core/placeholders/reportes.html')


#Logica para ver el panel segun el rol del usuario
@login_required
def panel_view(request):
    return render(request, 'core/includes/panel.html')


@login_required
def superadmin_dashboard(request):
    if not request.user.is_superadmin():
        return redirect('home')
    return render(request, 'core/_panel_superadmin.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_admin() and not request.user.is_superadmin():
        return redirect('home')
    return render(request, 'core/_panel_admin.html')

@login_required
def client_dashboard(request):
    if not request.user.is_cliente() and not request.user.is_superadmin():
        return redirect('home')
    return render(request, 'core/_panel_cliente.html')


#Redirige al home
def render_home(request):
    try:
        return render(request, 'core/home.html')
    except Exception as e:
        messages.error(request, f'Error al cargar la página principal: {e}')
        # Aún devolvemos la misma plantilla para no romper la navegación
        return render(request, 'core/home.html')

def pedidos_view(request):
    return render(request, 'core/pedidos.html')    

def catalogo_view(request):
    return render(request, 'catalogo.html')

def product_list(request):
    return render(request, 'products.html')

def render_home(request):
    try:
        return render(request, 'core/home.html')
    except Exception as e:
        messages.error(request, f'Error al cargar la página principal: {e}')
        # Aún devolvemos la misma plantilla para no romper la navegación
        return render(request, 'core/home.html')




# -----------------------
# 📌 Lista de productos
# -----------------------

# 📌 Listado con búsqueda y paginación
class ProductListView(View):
    template_name = "core/catalogo.html"

    def get(self, request):
        query = request.GET.get("q", "").strip() # búsqueda
        products = Product.objects.all()

        if query:
            # Buscar por nombre o categoría
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        # Paginación (6 productos por página)
        paginator = Paginator(products, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "query": query,
            "result_count": products.count()
        }
        return render(request, self.template_name, context)


# 📌 Crear producto
class ProductCreateView(View):
    template_name = "core/product_form.html"

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Producto creado exitosamente.")
                return redirect("product_catalog")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear el producto: {e}")
        return render(request, self.template_name, {"form": form})


# 📌 Editar producto
class ProductUpdateView(View):
    template_name = "core/product_form.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Producto actualizado correctamente.")
                return redirect("product_catalog")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {e}")
        return render(request, self.template_name, {"form": form})


# 📌 Eliminar producto
class ProductDeleteView(LoginRequiredMixin, View):
    template_name = "core/confirm_delete.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {"product": product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect("product_catalog")



#Papelera con borrado suave trabajar en otro momento
class ProductTrashView(View):
    template_name = "core/trash.html"

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, "Acceso denegado.")
            return redirect("product_catalog")

        products = Product.objects.filter(deleted_at__isnull=False)
        return render(request, self.template_name, {"products": products})
