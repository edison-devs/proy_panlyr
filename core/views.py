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
from .forms import ComprobantePagoForm

# Create your views here.


#Redirige al home
def render_home(request):
    try:
        return render(request, 'core/home.html')
    except Exception as e:
        messages.error(request, f'Error al cargar la página principal: {e}')
        # Aún devolvemos la misma plantilla para no romper la navegación
        return render(request, 'core/home.html')



#Logica para redirigir al panel de administración
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
# UPDATE PRODUCT
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
    

# --------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------------------------------------------------

def get_or_create_active_cart(user):
    """Obtiene o crea un carrito activo (pendiente) para el usuario"""
    if not user or not user.is_authenticated:
        raise ValueError("Se requiere un usuario autenticado para crear un carrito")
    
    status_pendiente, _ = CartStatus.objects.get_or_create(name="pendiente", defaults={"description": "Carrito pendiente"})
    
    # Buscar carrito activo existente
    cart = Cart.objects.filter(
        user=user,
        status=status_pendiente,
        deleted_at__isnull=True
    ).first()
    
    # Si no existe, crearlo
    if not cart:
        cart = Cart.objects.create(
            user=user,
            status=status_pendiente,
            quantity=0,
            price=0
        )
    
    return cart


# --------------------------------------------------------------------------------------------
# CATÁLOGO PÚBLICO
# --------------------------------------------------------------------------------------------

def catalogo_view(request):
    """Vista pública del catálogo de productos"""
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    products = Product.objects.filter(deleted_at__isnull=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Paginación (12 productos por página)
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        "page_obj": page_obj,
        "query": query,
        "categories": categories,
        "selected_category": category_id,
        "result_count": products.count()
    }
    return render(request, "core/catalogo.html", context)


# --------------------------------------------------------------------------------------------
# CARRITO DE COMPRAS
# --------------------------------------------------------------------------------------------

@login_required
def add_to_cart(request, product_id):
    """Agrega un producto al carrito"""
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id, deleted_at__isnull=True)
        quantity = int(request.POST.get("quantity", 1))
        
        if quantity <= 0:
            messages.error(request, "La cantidad debe ser mayor a 0.")
            return redirect("catalogo")
        
        cart = get_or_create_active_cart(request.user)
        
        # Verificar si el producto ya está en el carrito
        try:
            cart_product = CartProduct.objects.get(cart=cart, product=product)
            # Si ya existe, sumar la cantidad
            cart_product.quantity += quantity
            cart_product.save()
            messages.success(request, f"'{product.name}' agregado al carrito. Cantidad actualizada.")
        except CartProduct.DoesNotExist:
            # Si no existe, crearlo
            cart_product = CartProduct.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            messages.success(request, f"'{product.name}' agregado al carrito.")
        
        # Recalcular totales del carrito
        cart.calculate_total()
        
        # Redirigir de vuelta al catálogo para permitir seguir comprando
        return redirect("catalogo")
    return redirect("catalogo")


@login_required
def cart_view(request):
    """Vista del carrito de compras"""
    cart = get_or_create_active_cart(request.user)
    cart_items = cart.cart_products.all()
    total = cart.get_total()
    total_quantity = cart.get_total_quantity()
    
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total": total,
        "total_quantity": total_quantity,
    }
    return render(request, "core/cart.html", context)


@login_required
def update_cart_item(request, item_id):
    """Actualiza la cantidad de un producto en el carrito"""
    if request.method == "POST":
        cart_item = get_object_or_404(CartProduct, pk=item_id, cart__user=request.user)
        quantity = int(request.POST.get("quantity", 1))
        
        if quantity <= 0:
            messages.error(request, "La cantidad debe ser mayor a 0.")
            return redirect("cart_view")
        
        cart_item.quantity = quantity
        cart_item.save()
        
        # Recalcular totales del carrito
        cart_item.cart.calculate_total()
        
        messages.success(request, "Cantidad actualizada.")
    return redirect("cart_view")


@login_required
def remove_from_cart(request, item_id):
    """Elimina un producto del carrito"""
    if request.method == "POST":
        cart_item = get_object_or_404(CartProduct, pk=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart = cart_item.cart  # Guardar referencia al carrito antes de eliminar
        cart_item.delete()
        
        # Recalcular totales del carrito
        cart.calculate_total()
        
        messages.success(request, f"'{product_name}' eliminado del carrito.")
    return redirect("cart_view")


# --------------------------------------------------------------------------------------------
# REALIZAR PEDIDO (actualizado)
# --------------------------------------------------------------------------------------------

@login_required
def realizar_pedido(request):
    """Vista para realizar un pedido desde el carrito"""
    cart = get_or_create_active_cart(request.user)
    cart_items = cart.cart_products.all()
    
    if not cart_items.exists():
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de realizar un pedido.")
        return redirect("cart_view")
    
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            metodo_pago = data["metodo_pago"]
            direccion = data["direccion"]
            
            # Verificar si el método de pago es transferencia
            metodo_pago_nombre = metodo_pago.name.lower()
            es_transferencia = metodo_pago_nombre in ["transferencia", "transferencia bancaria", "pago movil", "pago móvil"]
            
            # Determinar el estado inicial del pedido
            if es_transferencia:
                # Si es transferencia, el pedido queda en "comprobante de pago requerido"
                tipo_pedido, _ = OrderType.objects.get_or_create(
                    name="comprobante de pago requerido",
                    defaults={"description": "Pedido esperando comprobante de pago"}
                )
                mensaje_exito = "Pedido realizado exitosamente. Por favor, sube el comprobante de pago para que tu pedido pueda ser procesado."
            else:
                # Si no es transferencia, el pedido queda en "pendiente"
                tipo_pedido, _ = OrderType.objects.get_or_create(
                    name="pendiente",
                    defaults={"description": "Pedido pendiente de aprobación"}
                )
                mensaje_exito = "Pedido realizado exitosamente. El administrador revisará tu pedido."
            
            # Actualizar estado del carrito a "completado"
            estado_completado, _ = CartStatus.objects.get_or_create(
                name="completado", 
                defaults={"description": "Carrito completado"}
            )
            
            # Crear entrega
            entrega = Delivery.objects.create(user=request.user, secondary_address=direccion)
            
            # Actualizar carrito
            cart.status = estado_completado
            cart.calculate_total()
            cart.save()
            
            # Crear pedido
            pedido = Order.objects.create(
                user=request.user,
                cart=cart,
                order_type=tipo_pedido,
                payment_method=metodo_pago,
                delivery=entrega
            )
            
            messages.success(request, mensaje_exito)
            return redirect("detalle_pedido", order_id=pedido.id)
    else:
        form = PedidoForm()
        # Pre-llenar con datos del usuario si existen
        if request.user.address:
            initial_data = {"direccion": request.user.address}
        else:
            initial_data = {}
        form = PedidoForm(initial=initial_data)
    
    context = {
        "form": form,
        "cart": cart,
        "cart_items": cart_items,
        "total": cart.get_total(),
        "total_quantity": cart.get_total_quantity(),
    }
    return render(request, "core/realizar_pedido.html", context)


# --------------------------------------------------------------------------------------------
# MIS PEDIDOS
# --------------------------------------------------------------------------------------------

@login_required
def mis_pedidos(request):
    """Vista para listar los pedidos del usuario"""
    orders = Order.objects.filter(
        user=request.user,
        deleted_at__isnull=True
    ).select_related('order_type', 'payment_method', 'delivery', 'cart').prefetch_related('cart__cart_products__product')
    
    # Paginación (10 pedidos por página)
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "orders": page_obj,
        "page_obj": page_obj,
    }
    return render(request, "core/mis_pedidos.html", context)


@login_required
def detalle_pedido(request, order_id):
    """Vista para ver los detalles de un pedido específico"""
    order = get_object_or_404(
        Order,
        pk=order_id,
        user=request.user,
        deleted_at__isnull=True
    )
    
    # Obtener los items del carrito
    cart_items = order.get_cart_items()
    total = order.get_total()
    total_quantity = order.get_total_quantity()
    
    # Formulario para subir comprobante (si es necesario)
    comprobante_form = None
    if order.esperando_comprobante() and not order.tiene_comprobante():
        comprobante_form = ComprobantePagoForm(instance=order)
    
    context = {
        "order": order,
        "cart_items": cart_items,
        "total": total,
        "total_quantity": total_quantity,
        "comprobante_form": comprobante_form,
    }
    return render(request, "core/detalle_pedido.html", context)


@login_required
def subir_comprobante(request, order_id):
    """Vista para subir el comprobante de pago"""
    order = get_object_or_404(
        Order,
        pk=order_id,
        user=request.user,
        deleted_at__isnull=True
    )
    
    # Verificar que el pedido necesita comprobante y está esperando
    if not order.esperando_comprobante():
        messages.error(request, "Este pedido no requiere comprobante de pago.")
        return redirect("detalle_pedido", order_id=order_id)
    
    if order.tiene_comprobante():
        messages.info(request, "Este pedido ya tiene un comprobante de pago subido.")
        return redirect("detalle_pedido", order_id=order_id)
    
    if request.method == "POST":
        form = ComprobantePagoForm(request.POST, request.FILES, instance=order)

        if not request.FILES.get("comprobante_pago"):  
            #messages.error(request, "Debes seleccionar un archivo antes de subir el comprobante.")
            return redirect("detalle_pedido", order_id=order_id)

        if form.is_valid():
            # Guardar el comprobante
            form.save()
            
            # Cambiar el estado del pedido a "pendiente"
            tipo_pendiente, _ = OrderType.objects.get_or_create(
                name="pendiente",
                defaults={"description": "Pedido pendiente de aprobación"}
            )
            order.order_type = tipo_pendiente
            order.save()
            
            messages.success(request, "Comprobante de pago subido exitosamente. Tu pedido está ahora pendiente de aprobación.")
            return redirect("detalle_pedido", order_id=order_id)
        else:
            messages.error(request, "Hubo un error al subir el comprobante. Por favor, verifica el archivo.")
    else:
        form = ComprobantePagoForm(instance=order)
    
    context = {
        "order": order,
        "form": form,
    }
    return render(request, "core/subir_comprobante.html", context)

