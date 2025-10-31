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
from .forms import PedidoForm

# Create your views here.
#placeholder vistas sencillas para mas adelante estilizar:

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

def render_home1(request):
    try:
        return render(request, 'core/home1.html')
    except Exception as e:
        messages.error(request, f'Error al cargar la página principal: {e}')
        # Aún devolvemos la misma plantilla para no romper la navegación
        return render(request, 'core/home1.html')

@login_required
def dashboard(request):
        return render(request, 'core/sidebar/index.html')

# --------------------------------------------------------------------------------------------
# INDEX PRODUCT
# --------------------------------------------------------------------------------------------

class ProductListView(View):
    template_name = "core/sidebar/products/index.html"

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


# --------------------------------------------------------------------------------------------
# CREATE PRODUCT
# --------------------------------------------------------------------------------------------

class ProductCreateView(View):
    template_name = "core/sidebar/products/create.html"

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                return redirect("product-create")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear el producto: {e}")
        return render(request, self.template_name, {"form": form})


# --------------------------------------------------------------------------------------------
# DELETE PRODUCT
# --------------------------------------------------------------------------------------------

class ProductUpdateView(View):
    template_name = "core/sidebar/products/update.html"

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
                return redirect("product-index")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {e}")
        return render(request, self.template_name, {"form": form})


# --------------------------------------------------------------------------------------------
# DELETE PRODUCT
# --------------------------------------------------------------------------------------------

class ProductDeleteView(LoginRequiredMixin, View):
    template_name = "core/confirm_delete.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {"product": product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect("product-index")



#Papelera con borrado suave trabajar en otro momento
class ProductTrashView(View):
    template_name = "core/trash.html"

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, "Acceso denegado.")
            return redirect("product-index")

        products = Product.objects.filter(deleted_at__isnull=False)
        return render(request, self.template_name, {"products": products})
    

@login_required
def realizar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            producto = data["producto"]
            cantidad = data["cantidad"]
            metodo_pago = data["metodo_pago"]
            tipo_pedido = data["tipo_pedido"]
            direccion = data["direccion"]

            estado_carrito = CartStatus.objects.get(name="pendiente")
            motivo_salida = OutputReason.objects.get(name="pedido")

            precio_total = producto.price * cantidad
            carrito = Cart.objects.create(status=estado_carrito, quantity=cantidad, price=precio_total)
            CartProduct.objects.create(cart=carrito, product=producto, quantity=cantidad)
            entrega = Delivery.objects.create(user=request.user, secondary_address=direccion)

            pedido = Order.objects.create(
                user=request.user,
                cart=carrito,
                order_type=tipo_pedido,
                payment_method=metodo_pago,
                delivery=entrega
            )

            Output.objects.create(
                product=producto,
                order=pedido,
                reason=motivo_salida,
                quantity=cantidad,
                description="Salida por pedido"
            )

            messages.success(request, "Pedido realizado exitosamente.")
            return redirect("mis_pedidos")
    else:
        form = PedidoForm()

    return render(request, "core/realizar_pedido.html", {"form": form})

